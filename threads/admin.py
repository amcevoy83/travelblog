from django.contrib import admin
from .models import Thread, Subject, Posts

# Register your models here.

admin.site.register(Thread)
admin.site.register(Posts)
admin.site.register(Subject)