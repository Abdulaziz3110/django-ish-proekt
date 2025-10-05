from django.shortcuts import render
from .models import Xodim, Mahsulot, IshKuni
from django.db.models import Sum
from datetime import date

def home(request):
    return render(request, 'index.html')

def index(request):
    return render(request, "index.html")

def xodimlar(request):
    xodimlar = Xodim.objects.all()
    for x in xodimlar:
        x.maosh = x.umumiy_maosh()
    return render(request, "xodimlar.html", {"xodimlar": xodimlar})


def mahsulotlar(request):
    mahsulotlar = Mahsulot.objects.all()
    return render(request, "mahsulotlar.html", {"mahsulotlar": mahsulotlar})

def ish_kunlari(request):
    ish_kunlari = IshKuni.objects.all()
    return render(request, "ish_kunlari.html", {"ish_kunlari": ish_kunlari})

def hisobot(request):
    boshlanish = request.GET.get('boshlanish')
    tugash = request.GET.get('tugash')

    ishlar = IshKuni.objects.select_related('xodim', 'mahsulot').all()

    # Agar foydalanuvchi sana tanlasa, filtrlaymiz
    if boshlanish and tugash:
        ishlar = ishlar.filter(sana__range=[boshlanish, tugash])

    # Xodimlar bo‘yicha umumiy summani hisoblash
    natija = {}
    jami_summa = 0
    for i in ishlar:
        summa = i.mahsulot.narxi * i.soni
        jami_summa += summa
        if i.xodim in natija:
            natija[i.xodim] += summa
        else:
            natija[i.xodim] = summa

    return render(request, "hisobot.html", {
        "natija": natija,
        "jami_summa": jami_summa,
        "boshlanish": boshlanish,
        "tugash": tugash
    })

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    xodimlar_soni = Xodim.objects.count()
    mahsulotlar_soni = Mahsulot.objects.count()
    ishlar_soni = IshKuni.objects.count()
    jami_tikilgan = sum(i.soni for i in IshKuni.objects.all())

    return render(request, 'ish/admin_dashboard.html', {
        'xodimlar_soni': xodimlar_soni,
        'mahsulotlar_soni': mahsulotlar_soni,
        'ishlar_soni': ishlar_soni,
        'jami_tikilgan': jami_tikilgan,
    })
