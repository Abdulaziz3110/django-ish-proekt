from django.contrib import admin
from .models import Xodim, Mahsulot, IshKuni

@admin.register(Xodim)
class XodimAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'bolim', 'lavozim', 'telefon')
    search_fields = ('ism', 'familiya', 'lavozim', 'bolim')

@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'model', 'narxi')

@admin.register(IshKuni)
class IshKuniAdmin(admin.ModelAdmin):
    list_display = ('xodim', 'mahsulot', 'soni', 'sana')
    list_filter = ('sana', 'xodim')