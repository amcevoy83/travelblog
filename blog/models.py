from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    class Meta:
        app_label = "blog"

    #our author is linked to a registered user in the 'auth_user' table
    author = models.ForeignKey('settings.AUTH_USER_MODEL')
    post_title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    #iniitially set the published date to blank and null. This will be then updated in the publish function below
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0)

    tag = models.CharField(max_length=30, blank=True, null=True)

    image = models.ImageField(upload_to="images", blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.post_title

class Suggestions(models.Model):
    class Meta:
        app_label = "blog"

    #our author is linked to a registered user in the 'auth_user' table
    author = models.CharField(max_length=255)
    post_title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    #iniitially set the published date to blank and null. This will be then updated in the publish function below
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0)

    tag = models.CharField(max_length=30, blank=True, null=True)

    image = models.ImageField(upload_to="images", blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.post_title
