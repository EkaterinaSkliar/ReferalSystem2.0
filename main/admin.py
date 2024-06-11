from django.contrib import admin

from main.models import User, SmsCode

admin.site.register(User)
admin.site.register(SmsCode)