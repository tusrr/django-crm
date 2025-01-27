from django.contrib import admin
from .models import Client,Comments,ClientFile
# Register your models here.

admin.site.register(Client)
admin.site.register(Comments)
admin.site.register(ClientFile)