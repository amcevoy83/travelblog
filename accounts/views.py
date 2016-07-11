import user
from arrow import arrow
from django.core.management.commands.loaddata import humanize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.conf import settings
import stripe
import datetime
import json
import arrow
from accounts.models import User
from backends import SubscriptionEnded

stripe.api_key = settings.STRIPE_SECRET
# Create your views here.

#SINGLE PAYMENT ONLY
#  def register(request):
#     #if we have a post to the url then populate the registration form with the request.POST information
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#
#             try:
#                 #send web services call to stripe - makes association with credit card and customer
#                 customer = stripe.Charge.create(
#                     amount = 499,
#                     currency = "EUR",
#                     description = form.cleaned_data['email'],
#                     card = form.cleaned_data['stripe_id'],
#                     plan = 'REG_MONTHLY',
#                 )
#                # print "IM THE CUSTOMER", json.dumps(customer)
#
#             except stripe.error.CardError, e:
#                 messages.error(request, "Your (valid) card was declined!")
#
#             if customer.paid:
#                 form.save()
#                 user = auth.authenticate(email=request.POST.get('email'),
#                                          password = request.POST.get('password1'))
#
#                 if user:
#                     auth.login(request,user)
#
#                     messages.success(request, "You have successfully registered. Your customer id number is")
#                     return redirect(reverse('profile'))
#                 else:
#                     messages.error(request,'Unable to log you in at this time!')
#             else:
#                 messages.error(request, "We were unable to take a payment with that card!")
#     #if not then show a blank form
#     else:
#         today = datetime.date.today()
#         # form = register_form()
#         form = UserRegistrationForm(initial = {'expiry_month':today.month,
#                                                'expiry_year':today.year})
#
#     args = {'form':form, 'publishable': settings.STRIPE_PUBLISHABLE}
#     args.update(csrf(request))
#
#     return render(request, 'register.html', args)


#SUBSCRIPTION PAYMENT
def register(request):
    #if we have a post to the url then populate the registration form with the request.POST information
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            try:
                customer = stripe.Customer.create(
                    email = form.cleaned_data['email'],
                    card = form.cleaned_data['stripe_id'],
                    plan = 'REG_MONTHLY',
                )

            except stripe.error.CardError, e:
                messages.error(request, "Your (valid) card was declined!")

            if customer:
                user = form.save()
                user.stripe_id = customer.id
                user.subscription_end = arrow.now().replace(weeks=+4).datetime
                user.save()

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
        form = UserRegistrationForm(initial = {'expiry_month':today.month,
                                               'expiry_year':today.year})

    args = {'form':form, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'register.html', args)

@login_required(login_url='/accounts/login/')
def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        customer.cancel_subscription(at_period_end=True)

    except Exception,e:
        messages.error(request,e)

    return redirect('profile')

@csrf_exempt
def subscriptions_webhook(request):
    #turn our request.body in to a dictionary so we can easily pull out the values from the file
    event_json = json.loads(request.body)

    #Verify the event by fetching it from Stripe
    try:
        #firstly verify this is a real event generated by Stripe.com, if it is then assign it to the variable 'event'
        event = stripe.Event.retrieve(event_json["id"])

        #get our user by the customer string (this pulls the User class defined in our models which looks for the inputted stripe_id from the form that was input.
        user = User.objects.get(stripe_id=event_json["data"]["object"]["customer"])

        if user and event_json ['type']=="invoice.payment_succeeded":
            user.subscription_end = arrow.now().replace(weeks=+4).datetime
            user.save()

    except stripe.InvalidRequestError, e:
        return HttpResponse(status=404)

    return HttpResponse(status=200, content="sucess")

def login(request, success_url=None):

    if request.user.is_authenticated():
        return redirect(reverse('profile'))

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                user = auth.authenticate(email=request.POST.get('email'),
                                         password=request.POST.get('password'))
                if user is not None:
                    auth.login(request, user)
                    messages.error(request, "You have successfully logged in")
                    return redirect(reverse('profile'))
                else:
                    subscription_not_ended = arrow.now() < arrow.get(user.subscription_end)

                    if not subscription_not_ended:
                        form.add_error(None,"Your subscription has now ended")

                    form.add_error(None,"Your email or password was not recognised")

            except SubscriptionEnded:
                form.add_error(None,"Your subscription has now ended")

    else:
        form = UserLoginForm()

    args = {'form':form}
    args.update(csrf(request))
    return render(request, 'login.html', args)

@login_required(login_url ='login/')
def profile(request):
    subscription_humanize = arrow.get(request.user.subscription_end).humanize()
    login_humanize = arrow.get(request.user.date_joined).humanize()
    args = {'subscription_humanize':subscription_humanize, 'login_humanize':login_humanize}
    return render(request,'profile.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return render(request, 'core/index.html')