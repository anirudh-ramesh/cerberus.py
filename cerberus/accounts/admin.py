from django.contrib import admin
from accounts.models import User, Email


admin.site.register(User)
admin.site.register(Email)