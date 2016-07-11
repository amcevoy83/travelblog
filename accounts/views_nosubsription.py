from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.conf import settings
import stripe
import datetime
import json

stripe.api_key = settings.STRIPE_SECRET
# Create your views here.

def register(request):
    #if we have a post to the url then populate the registration form with the request.POST information
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            try:
                #send web services call to stripe - makes association with credit card and customer
                customer = stripe.Charge.create(
                    amount = 499,
                    currency = "EUR",
                    description = form.cleaned_data['email'],
                    card = form.cleaned_data['stripe_id'],
                )
               # print "IM THE CUSTOMER", json.dumps(customer)

            except stripe.error.CardError, e:
                messages.error(request, "Your (valid) card was declined!")

            if customer.paid:
                form.save()
                user = auth.authenticate(email=request.POST.get('email'),
                                         password = request.POST.get('password1'))

                if user:
                    auth.login(request,user)

                    messages.success(request, "You have successfully registered. Your customer id number is")
                    return redirect(reverse('profile'))
                else:
                    messages.error(request,'Unable to log you in at this time!')
            else:
                messages.error(request, "We were unable to take a payment with that card!")
    #if not then show a blank form
    else:
        today = datetime.date.today()
        # form = register_form()
        form = UserRegistrationForm(initial = {'expiry_month':today.month,
                                               'expiry_year':today.year})

    args = {'form':form, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'register.html', args)

def login(request, success_url=None):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))
            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(reverse('profile'))
            else:
                form.add_error(None,"Your email or password was not recognised")
    else:
        form = UserLoginForm()

    args = {'form':form}
    args.update(csrf(request))
    return render(request, 'login.html', args)

@login_required(login_url ='login/')
def profile(request):
 #    user = auth.authenticate(email=request.POST.get('email'),
 #                                     password=request.POST.get('password'), stripe_id = request.POST.get('stripe_id'))
 #    if 'user.stripe_id' == "tok_17G9pXGNQXKVOz9UpFARYnJP":
 # #   if user.stripe_id == "aoifemcevoy@gmail.com":
 #        messages.success(request, "Nice one")
 #        print "Whoop"
 #    else:
 #        messages.success(request, "Not today")
 #    retrieve = stripe.Charge.retrieve("ch_17G9QUGNQXKVOz9Ur51tzCLe")
 #    #retrieve = stripe.Charge.retrieve[id]
 #    newid = retrieve.created
 #    args = messages.success(request, "CREATED BY:", newid)
 #    args.update(csrf(request))
    # print retrieve
    return render(request,'profile.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return render(request, 'index.html')