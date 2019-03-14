from django.contrib import admin
from configsetting.models import GlobalPreference


class GlobalPreferenceAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')


admin.site.register(GlobalPreference, GlobalPreferenceAdmin)
