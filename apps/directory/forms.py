from django import forms
from django.forms.widgets import TextInput
from django.shortcuts import get_object_or_404

from directory.models import Club
from directory.models import City
from directory.models import State

class ClubForm(forms.ModelForm):
    # make coord read only.
    longitude = forms.DecimalField(required=False, widget=TextInput(attrs={'readonly': True}))
    latitude = forms.DecimalField(required=False, widget=TextInput(attrs={'readonly': True}))
    class Meta:
        model = Club
        #fields =  ('name', 'description', 'address', 'email', 'homepage')
                    # all (name, description, address, state, city, phone, 
                    # email, homepage, latitude, longitude, rating, 
                    # date_of_review, is_closed, objects, current_site_only, 
                    # open_only, sites, owner
        exclude = ('sites', 'owner', 'date_of_review', 'rating', 'is_closed')
    
    def __init__(self, *args, **kwargs):
        super(ClubForm,self ).__init__(*args,**kwargs) 

        # if form is bound, it contains state id. filter cities by this state.
        if self.is_bound:
            state_id = self.data.get("state", None) 
            if state_id:
                state = get_object_or_404(State, id=state_id)
                self.fields["city"].queryset = state.city_set.all()
            else:
                self.fields["city"].queryset = City.objects.none()
                
        else:
            # club is saved already. filter cities by club's state
            club = kwargs.get("instance", None)
            if club:
                self.fields["city"].queryset = club.state.city_set.all()
            else:
                self.fields["city"].widget.attrs["disabled"] = True
                self.fields["city"].queryset = City.objects.none()
            

