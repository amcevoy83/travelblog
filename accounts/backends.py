import datetime
from models import User
import arrow
#This class replaces the standard 'auth' object that django uses to check logins. We are overridinig two of it's default methods
class SubscriptionEnded(Exception):
    pass

class EmailAuth(object):
    def authenticate(self, email=None, password=None):
         # """ Get an insatnce of User using the supplied email and check it's password""
        try:
            user = User.objects.get(email=email)

            subscription_not_ended = arrow.now() < arrow.get(user.subscription_end)
            if not subscription_not_ended:
                raise SubscriptionEnded()

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None

        except User.DoesNotExist:
            return None
