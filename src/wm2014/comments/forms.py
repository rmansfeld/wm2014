from django import forms
from .models import Tip, Comment


class TipForm(forms.ModelForm):
    guess_widget = forms.TextInput(attrs={'class': 'guess', 'size': '2',
                                          'maxlength': '2'})
    guess1 = forms.IntegerField(widget=guess_widget, required=False)
    guess2 = forms.IntegerField(widget=guess_widget, required=False)

    class Meta:
        model = Tip
        fields = ['guess1', 'guess2']


class CommentForm(forms.Form):
    TEXTAREA_ATTRS = {'cols': '50', 'rows': '15'}
    text = forms.CharField(widget=forms.Textarea(attrs=TEXTAREA_ATTRS))

    class Meta:
        model = Comment
        fields = ['text']


class TestForm(forms.Form):
    test_time = forms.DateTimeField()
