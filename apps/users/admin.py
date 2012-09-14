# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from apps.users.models import Profile, ProfileAddress
admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile

class ProfileAddressInline(admin.StackedInline):
    model = ProfileAddress

class MyAdmin(UserAdmin):
    list_display = ('id','email','is_staff',)
    list_display_links = ('id','email',)
    inlines = [ProfileInline, ProfileAddressInline]

admin.site.register(User, MyAdmin)
