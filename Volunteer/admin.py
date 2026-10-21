from django.contrib import admin
from .models import Admin, Committee, Volunteer, Event, TaskApplication


# Register your models here.
# Register each model
admin.site.register(Admin)
admin.site.register(Committee)
admin.site.register(Volunteer)
admin.site.register(Event)
admin.site.register(TaskApplication)