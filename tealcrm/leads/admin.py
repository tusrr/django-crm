from django.contrib import admin
from .models import Lead,Comments,LeadFile
# Register your models here.
admin.site.register(Lead)
admin.site.register(Comments)
admin.site.register(LeadFile)