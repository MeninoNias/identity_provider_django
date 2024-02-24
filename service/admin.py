from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.urls import path, reverse
from django.http import HttpResponse

from service.models import User, IdentityClient

class BaseAdmin(admin.ModelAdmin):
    queryset_class = None

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ()

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
    actions = ['export_csv',]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    def export_csv(self, request, queryset):
        titles = (u'username', u'password',)
        csv = u"%s\n" % u",".join([u'"%s"' % item for item in titles])
        for obj in queryset:
            row = (
                obj.email,
                '123456',
            )
            csv += u"%s\n" % u",".join([u'"%s"' % item for item in row])
        response = HttpResponse(csv.encode(
            'utf-8'), content_type='application/csv; charset=utf-8', )
        response['Content-Disposition'] = 'filename=users.csv'
        return response

    export_csv.short_description = u'Exportar CSV'
    
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


@admin.register(IdentityClient)
class IdentityClientAdmin(BaseAdmin):
    queryset_class = IdentityClient
    list_display = ['name', 'app_id', 'api_key',]
    ordering = ['name',]
    search_fields = ['app_id', 'name', 'api_key',]
    readonly_fields = ['app_id', 'api_key',]