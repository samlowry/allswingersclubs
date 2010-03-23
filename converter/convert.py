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
pat = re.compile(r"http://[\w.]*allswingersclubs.org/club/(?P<club_id>\d+)/.*")

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

            club_guid = pat.match(guid)
            if club_guid:
                club_id = club_guid.groupdict()["club_id"]
            else:
                log("%s doesnt match with pattern" % guid)
                continue
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
                if len(comment.comment) != len(comment_info["comment"]):
                    print len(comment.comment), "-", len(comment_info["comment"])
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

    
def replace_amp():
    """ replaces html entities within user_name or comment """
    comments = Comment.objects.filter(submit_date__lt="2010-03-17")
    counter = 0
    replaced_counter = 0
    for comment in comments:
        # replace &amp; in the username
        if comment.user_name.find("&amp;") >= 0:
            comment.user_name = comment.user_name.replace("&amp;", "&")
            comment.save()
            print "user_name - %s changed" % comment.user_name
            
        if comment.comment.find(";") >= 0:
            counter = counter + 1

            if comment.comment.find("&#039;") >= 0:
                comment.comment = comment.comment.replace("&#039;", "'")
                comment.save()
                replaced_counter = replaced_counter + 1
                
            if comment.comment.find("&amp;") >= 0:
                comment.comment = comment.comment.replace("&amp;", "&")
                comment.save()
                replaced_counter = replaced_counter + 1
                  
            if comment.comment.find("&lt;") >= 0:
                comment.comment = comment.comment.replace("&lt;", "<")
                comment.save()
                replaced_counter = replaced_counter + 1
                  
            if comment.comment.find("&lsquo;") >= 0:
                comment.comment = comment.comment.replace("&lsquo;", "'")
                comment.save()
                replaced_counter = replaced_counter + 1
                                  
            if comment.comment.find("&rsquo;") >= 0:
                comment.comment = comment.comment.replace("&rsquo;", "'")
                comment.save()
                replaced_counter = replaced_counter + 1
                       
            if comment.comment.find("&quot;") >= 0:
                comment.comment = comment.comment.replace('&quot;', '"')
                comment.save()
                replaced_counter = replaced_counter + 1
                                    
    print "found %s comments with semicolons" % counter
    print "replaced %s entities" % replaced_counter
