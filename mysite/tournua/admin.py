from django.contrib import admin
from .models import UserAccount, Tournament, Team

admin.site.register(UserAccount)
admin.site.register(Tournament)
admin.site.register(Team)