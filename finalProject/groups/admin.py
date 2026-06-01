from django.contrib import admin
from .models import group, assignment, assignmentGroup

# Register your models here.
admin.site.register(group)
admin.site.register(assignment)
admin.site.register(assignmentGroup)