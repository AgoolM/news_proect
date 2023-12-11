from django import forms
from .models import Contact,Comsent


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"  

class CommentForm(forms.ModelForm):


    class Meta:
        model = Comsent
        fields = ['body']