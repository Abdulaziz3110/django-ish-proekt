from django.contrib import admin
from .models import Xodim, Mahsulot, IshKuni

@admin.register(Xodim)
class XodimAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'user', 'bolim', 'lavozim', 'telefon', 'is_approved')
    list_filter = ('is_approved', 'bolim', 'lavozim')
    search_fields = ('ism', 'familiya', 'user__username', 'telefon')
    list_editable = ('is_approved',)
    actions = ['approve_xodimlar', 'disapprove_xodimlar']

    @admin.action(description="Tanlangan xodimlarni tasdiqlash")
    def approve_xodimlar(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Tanlangan xodimlarni tasdiqdan chiqarish")
    def disapprove_xodimlar(self, request, queryset):
        queryset.update(is_approved=False)


@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'model', 'narxi')

@admin.register(IshKuni)
class IshKuniAdmin(admin.ModelAdmin):
    list_display = ('xodim', 'mahsulot', 'soni', 'sana')
    list_filter = ('sana', 'xodim')