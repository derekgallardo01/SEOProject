from django.contrib import admin
from .models import ShortURL
# Register your models here.


class ShortURLAdmin(admin.ModelAdmin):
    list_per_page = 20
    fields = ['code',('recordid','tablename'),'recordname']
    list_display = ('code', 'recordid', 'recordname', 'tablename','status')

    def custom_amenities_display(self, obj):
        return mark_safe("Amenities can only be modified by special request, please contact the store manager at %s to create a request" % (obj.email,obj.email))
    custom_amenities_display.short_description = "Amenities"

admin.site.register(ShortURL, ShortURLAdmin)
