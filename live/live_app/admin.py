from django.contrib import admin
from .models import Property, PropertyType, PropertyImage, Comment


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyType)
admin.site.register(Comment)