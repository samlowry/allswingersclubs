# -*- coding: utf-8 -*-
# usage:
#   manage.py shell
#   from converter import convert
#   convert.main()
#   Each start adds (not replaces) comments to the django.
import xml.dom.minidom
import datetime
from directory.models import Club
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment

import re
# print content
pat = re.compile(r"http://allswingersclubs.org/club/(?P<club_id>\d+)/.*")

def main():
    # empty check file
    f = open("converter/check.txt", "w")
    f.close()

    #empty log file
    f = open("converter/log.txt", "w")
    f.close()

    # check is csv file
    check_file(("guid", "xml_club_id", "django_club_id", "xml_user_name", "django_user_name", "xml_user_email", "django_user_email",
    "xml_comment", "django_comment", "xml_created_gmt", "django_created_est",))
    parsed_xml = xml.dom.minidom.parse("converter/dump.xml")

    parsed_xml.normalize()

    converted_posts_counter = 0
    all_comments = parsed_xml.getElementsByTagName("email")
    try:
        blogposts = parsed_xml.getElementsByTagName("blogpost")
        for post in blogposts:

            amount = 0
            post_info = dict(map(node_to_tuple, post.childNodes))

            guid = post_info["guid"]
            if len(guid) == 0:
                raise Exception("guid is empty")
            print "processing %s " % guid
            # get club

            club_id = pat.match(guid).groupdict()["club_id"]
            try:
                club = Club.objects.get(id=club_id)
            except club.DoesNotExist:
                log("Club with id %s does not exists (guid=%s)" % (club_id, guid))
                continue

            # get content type of club
            club_ct = ContentType.objects.get_for_model(club)

            all_emails = post.getElementsByTagName("email")

            for email in all_emails:
                amount = amount + 1
                comment_node = email.parentNode
                comment_info = dict(map(node_to_tuple, comment_node.childNodes))
                comment = Comment()
                comment.content_type_id = club_ct.id
                comment.object_pk = club_id
                comment.site_id = 1
                comment.user_name = comment_info["name"]
                comment.user_email = comment_info["email"]
                comment.comment = comment_info["comment"]

                # converting string to datetime object
                dt = datetime.datetime.strptime(comment_info["gmt"], "%Y-%m-%d %H:%M:%S")

                # gmt to est. EST is GMT - 5 hours
                dt = dt - datetime.timedelta(hours=5)
                comment.submit_date = dt

                comment.save()
                converted_posts_counter = converted_posts_counter + 1
                # saving log
                check_file((guid, club_id, comment.object_pk, comment_info["name"], comment.user_name, comment_info["email"], comment.user_email,
                        comment_info["comment"], comment.comment, comment_info["gmt"], comment.submit_date,))
        log("%s clubs in the xml file" % len(blogposts))
        log("%s comments in the xml file" % len(all_comments))
        log("%s comments converted" % converted_posts_counter)
    except Exception, exc:
        log(str(exc))

def node_to_tuple(child):
    """ gets node, returns tuple (node name, node value) """
    try:
        node_value = child.firstChild.nodeValue.strip()
    except AttributeError:
        node_value = ""
    node_name = child.nodeName
    return (node_name, node_value,)

def check_file(log_tuple):
    f = open("converter/check.txt", "a")
    log_tuple = (str(t) for t in log_tuple)
    f.write("|".join(log_tuple))
    f.write("\n")
    f.close()

def log(log_str):
    f = open("converter/log.txt", "a")
    f.write(log_str)
    f.write("\n")
    f.close()
