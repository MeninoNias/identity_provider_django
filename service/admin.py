from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.urls import path, reverse

from service.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    queryset_class = User
    change_user_password_template = None
    change_password_form = AdminPasswordChangeForm
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('get_full_name', 'email')
    search_fields = ('first_name', 'last_name', 'email',)
    fields = ('first_name', 'last_name', 'email', 'password',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    # def get_urls(self):
    #     return [
    #         path(
    #             '<id>/password/',
    #             self.admin_site.admin_view(self.user_change_password),
    #             name='auth_user_password_change',
    #         ),
    #     ] + super().get_urls()
