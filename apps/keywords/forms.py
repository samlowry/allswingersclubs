from django import forms
from django.contrib.sites.models import Site

from keywords.models import KeywordState


class SearchForm(forms.Form):
    q = forms.CharField(label="")


class SiteAdminForm(forms.ModelForm):
    keywords_on = forms.BooleanField(initial=False, required=False)
    class Meta:
        model = Site
    def __init__(self, *args, **kwargs):
        super(SiteAdminForm, self).__init__(*args, **kwargs)
        is_on = False
        try:
            is_on = self.instance.keywordstate.is_on
        except KeywordState.DoesNotExist:
            pass
        self.fields["keywords_on"].initial = is_on 

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(SiteAdminForm, self).save(commit=False)
        if commit:
            m.save()
        kw_setting, created = KeywordState.objects.get_or_create(site=m)
        kw_setting.is_on = self.cleaned_data["keywords_on"]
        kw_setting.save()
        return m
