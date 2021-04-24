from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core import validators


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

class createProductForm(forms.Form):
	name = forms.CharField(label="Name", max_length=80)
	price = forms.FloatField(label="Price",validators=[validators.MinValueValidator(0), validators.MaxValueValidator(99999)])
	description = forms.CharField(widget=forms.Textarea(attr={'class':'alert alert-danger'}), label="Description", max_length=250)
	image = forms.FileField(label="Image")
	quantity = forms.IntegerField(label="Quantity",validators=[validators.MinValueValidator(0)])
	stock = forms.BooleanField(label="Stock")
	brand = forms.CharField(label="Brand", max_length=80)
	CATEGORY = (('Smartphones', 'Smartphones'),
				('Computers', 'Computers'),
				('Tablets', 'Tablets'),
				('Drones', 'Drones')
				, ('Televisions', 'Televisions'))