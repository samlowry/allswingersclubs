from django import forms
from directory.models import Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        #fields =  ('name', 'description', 'address', 'email', 'homepage')
                    # all (name, description, address, state, city, phone, 
                    # email, homepage, latitude, longitude, rating, 
                    # date_of_review, is_closed, objects, current_site_only, 
                    # open_only, sites, owner
        exclude = ('sites', 'owner', 'date_of_review', 'rating', 'is_closed')