from django.shortcuts import render, redirect
from .models import Xodim, Mahsulot, IshKuni
from django.db.models import Sum
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required

def home(request):
    return render(request, 'index.html')

def index(request):
    return render(request, "index.html")

def register_view(request):
    if request.method == "POST":
        ism = request.POST.get("ism")
        familiya = request.POST.get("familiya")
        username = request.POST.get("username")
        password = request.POST.get("password")
        bolim = request.POST.get("bolim")
        lavozim = request.POST.get("lavozim")
        telefon = request.POST.get("telefon")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Ushbu username band! Boshqa username tanlang."})

        # Foydalanuvchi yaratish
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=ism,
            last_name=familiya
        )

        # Xodim profilini yaratish va bazaga saqlash
        Xodim.objects.create(
            user=user,
            ism=ism,
            familiya=familiya,
            bolim=bolim,
            lavozim=lavozim,
            telefon=telefon,
            ishga_kirilgan_sana=date.today()
        )

        # Avtomatik login qilish
        login(request, user)
        return redirect("index")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"error": "Username yoki parol noto'g'ri!"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def xodimlar(request):
    if request.method == "POST":
        ism = request.POST.get("ism")
        familiya = request.POST.get("familiya")
        bolim = request.POST.get("bolim")
        lavozim = request.POST.get("lavozim")
        telefon = request.POST.get("telefon")
        ish_haqi = request.POST.get("ish_haqi") or 0
        ishga_kirilgan_sana = request.POST.get("ishga_kirilgan_sana") or None

        if ism and familiya:
            Xodim.objects.create(
                ism=ism,
                familiya=familiya,
                bolim=bolim,
                lavozim=lavozim,
                telefon=telefon,
                ish_haqi=ish_haqi,
                ishga_kirilgan_sana=ishga_kirilgan_sana if ishga_kirilgan_sana else None
            )
            return redirect("xodimlar")

    xodimlar = Xodim.objects.all().order_by('-id')
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

