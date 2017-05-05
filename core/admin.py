from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    exclude = ('metadata',)
