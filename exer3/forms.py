from django import forms
#from django.forms import extras
subject= [
    ('Software', 'Software'),
    ('Hardware', 'Hardware'),
    ('Networking', 'Networking'),
    ]

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class SearchForm(forms.Form):
    subject = forms.CharField(max_length=100)

class RegForm(forms.Form):
	name = forms.CharField(label='Name:', max_length=100)
	subject_list= forms.CharField(label='Subject:', widget=forms.Select(choices=subject))

class SubAdd(forms.Form):
	name = forms.CharField(label='Your name', max_length=100)