# from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from bbs_account.models import UserLTopic
from bbs_account.forms import RegistrationAskForm, UserChangeForm

MyUser = get_user_model()


class MyUserInline(admin.TabularInline):
    model = MyUser


class MyUserCreationForm(RegistrationAskForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar_img', 'address',
                                         'phone', 'born_date', 'coins', 'location', 'signature', 'post_count',
                                          'website', 'topic_count', 'time_zone',
                                         )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_activity', 'date_joined')}),
    )
    # inlines = [MyUserInline,]


admin.site.register(MyUser, MyUserAdmin)

admin.site.register(UserLTopic )


