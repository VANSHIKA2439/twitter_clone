from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile,Tweet
# Register your models here.
#remove groups
admin.site.unregister(Group)

#mix profile info with user info
class ProfileInline(admin.StackedInline):
    model = Profile

#for only showing username on site
class UserAdmin(admin.ModelAdmin):
    model =  User
    fields = ['username']
    inlines = [ProfileInline]

admin.site.unregister(User) 
admin.site.register(User,UserAdmin)
admin.site.register(Tweet)
#registering profile database or model
#admin.site.register(Profile)
#we wont register profile when we mix profile info with user info because user is already registered