from django.contrib import admin
from.models import Branch 
from.models import User_id
from.models import User_accounts
from.models import Transcations

# Register your models here.
admin.site.register(Branch)
admin.site.register(User_id)
admin.site.register(User_accounts)
admin.site.register(Transcations)