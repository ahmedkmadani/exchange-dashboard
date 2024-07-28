from django.contrib import admin
from .models import Currency, Wallet
# Register your models here.
admin.site.register(Wallet)
admin.site.register(Currency)