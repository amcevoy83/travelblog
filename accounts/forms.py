from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


# there is a default UserCreationForm already established in django which we use here. It knows the difference between email registration instead of username.
class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    credit_card_number = forms.CharField(
        label = 'Credit Card Number'
    )

    cvv = forms.CharField(
        label = 'Security Code (CVV)'
    )

    MONTH_CHOICES = [(i, i,)for i in xrange(1,13)]
    YEAR_CHOICES = [(i,i,)for i in xrange(2015,2036)]

    expiry_month = forms.ChoiceField(
        label = 'Month',
        choices = MONTH_CHOICES
    )

    expiry_year = forms.ChoiceField(
        label="Year",
        choices = YEAR_CHOICES
    )

    #this is hiddent as we are using it only internally to store the token returned by stripe later
    stripe_id = forms.CharField(
        widget = forms.HiddenInput
    )
    class Meta:
        # here we are only showing what fields we want to ie. the email and passwords, we're exluding usernanem
        model = User
        fields = ['email', 'password1', 'password2', 'stripe_id']
        exclude = ['username']


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = 'Passwords do not match'
            raise forms.ValidationError(message)
        return password2


    # We need to override the ordinary save function ... the original function used the AbstractUser class which insisted on a username field not being empty onn save. Now we need to over ride this as we are no longer requesting the username.
    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)
        # automatically set to email address to create a unique identifier(this is the difference between this and the standard save, here we reassign email instead of username)
        instance.username = instance.email
        if commit:
            instance.save()
        return instance


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
