from django import forms
from .models import Keyword, Trend

class KeywordForm(forms.ModelForm):
    name = forms.CharField(label="키워드")
    class Meta:
        model = Keyword
        fields = ('name',)


class TrendForm(forms.ModelForm):

    class Meta:
        model = Trend
        fields = '__all__'