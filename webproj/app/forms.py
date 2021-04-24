from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


def cardNo(value):
	if len(str(value)) != 12 or value<0:
		raise forms.ValidationError("Card Number Should Have 12 digits")


def cardCode(value):
	if len(str(value)) != 3 or value<0:
		raise forms.ValidationError("Card Code Should Have 3 digits")


def expirationYear(value):
	if len(str(value)) != 4 or value < 2021:
		raise forms.ValidationError("Card Expiration Year Should Be YYYY")

def expirationMonth(value):
	if value > 12 or value<=0:
		raise forms.ValidationError("Card Expiration Month Should Be MM")


class newUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']



class paymentForm(forms.Form):
	TYPES = (('Credit Card', 'Credit Card'), ('Debit Card','Debit Card'))
	type = forms.ChoiceField(choices= TYPES)
	card_no = forms.IntegerField(label='Card Number',validators =[cardNo])
	card_code = forms.IntegerField(label='Code', validators =[cardCode])
	expirationMonth = forms.IntegerField(label='Card Expiration Month',validators =[expirationMonth])
	expirationYear = forms.IntegerField(label='Card Expiration Year',validators =[expirationYear])
	address = forms.CharField(label='Address',max_length=250)


class updateUserForm(forms.Form):
	first_name = forms.CharField(label='First Name')
	last_name = forms.CharField(label='Last Name')
	username = forms.CharField(label='Username')
	email = forms.EmailField(label='Your Email')
	currentPassword = forms.CharField(label='Current Password', widget=forms.PasswordInput())
	newPassword = forms.CharField(label='New Password', widget=forms.PasswordInput())
	repeatNewPassword = forms.CharField(label='Repeat New Password', widget=forms.PasswordInput())


