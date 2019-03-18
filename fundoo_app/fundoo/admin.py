from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Profile, Notes, Labels, MapLabel

admin.site.register(Profile)
admin.site.register(Notes)
admin.site.register(Labels)
admin.site.register(MapLabel)


class NoteAdmin(admin.ModelAdmin):
    class Meta:
        model = Notes
