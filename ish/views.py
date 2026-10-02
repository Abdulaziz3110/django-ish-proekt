from django.shortcuts import render, redirect, get_object_or_404
from .models import Xodim, Mahsulot, IshKuni
from django.db.models import Sum
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif hasattr(request.user, 'xodim_profile'):
            return redirect('kabinet')
    return render(request, 'index.html')

def index(request):
    return render(request, "index.html")

def register_view(request):
    existing_xodimlar = Xodim.objects.filter(user__isnull=True)

    if request.method == "POST":
        ism = request.POST.get("ism")
        familiya = request.POST.get("familiya")
        username = request.POST.get("username")
        password = request.POST.get("password")
        bolim = request.POST.get("bolim")
        lavozim = request.POST.get("lavozim")
        telefon = request.POST.get("telefon")
        selected_xodim_id = request.POST.get("existing_xodim")

        # 1. Username allaqachon mavjudligini tekshirish
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Ushbu username band! Boshqa username tanlang.",
                "existing_xodimlar": existing_xodimlar
            })

        xodim = None
        if selected_xodim_id:
            xodim = Xodim.objects.filter(id=selected_xodim_id).first()
            if xodim and xodim.user is not None:
                return render(request, "register.html", {
                    "error": "Ushbu xodim uchun allaqachon akkaunt yaratilgan!",
                    "existing_xodimlar": existing_xodimlar
                })

        # 2. Ism, familiya va telefon orqali takroriy akkauntni tekshirish
        if not xodim and telefon:
            matched = Xodim.objects.filter(ism__iexact=ism, familiya__iexact=familiya, telefon=telefon).first()
            if matched:
                if matched.user is not None:
                    return render(request, "register.html", {
                        "error": f"{ism} {familiya} uchun allaqachon akkaunt yaratilgan!",
                        "existing_xodimlar": existing_xodimlar
                    })
                xodim = matched

        # 3. Foydalanuvchi yaratish (Parol xavfsiz hashlanadi)
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=ism,
            last_name=familiya
        )

        # 4. Xodim profiliga biriktirish yoki yangi yaratish (is_approved=False)
        if xodim:
            xodim.user = user
            xodim.ism = ism
            xodim.familiya = familiya
            if telefon:
                xodim.telefon = telefon
            if bolim:
                xodim.bolim = bolim
            if lavozim:
                xodim.lavozim = lavozim
            xodim.is_approved = False
            xodim.save()
        else:
            Xodim.objects.create(
                user=user,
                ism=ism,
                familiya=familiya,
                bolim=bolim,
                lavozim=lavozim,
                telefon=telefon,
                ishga_kirilgan_sana=date.today(),
                is_approved=False
            )

        return render(request, "register.html", {
            "success": "Ro'yxatdan muvaffaqiyatli o'tdingiz! Akkauntingiz admin tomonidan tasdiqlangach tizimga kira olasiz."
        })

    return render(request, "register.html", {"existing_xodimlar": existing_xodimlar})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")

            # Xodim profilini tekshirish
            xodim = getattr(user, 'xodim_profile', None)
            if xodim:
                if not xodim.is_approved:
                    return render(request, "login.html", {
                        "error": "Sizning akkauntingiz hali admin tomonidan tasdiqlanmagan. Iltimos, admin tasdiqlashini kuting."
                    })
                login(request, user)
                return redirect("kabinet")
            else:
                login(request, user)
                return redirect("index")
        else:
            return render(request, "login.html", {"error": "Username yoki parol noto'g'ri!"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def kabinet_view(request):
    user = request.user
    xodim = getattr(user, 'xodim_profile', None)

    if not xodim and not user.is_superuser:
        return redirect('index')

    if user.is_superuser and not xodim:
        # Admin uchun namuna sifatida birinchi xodimni ko'rsatish yoki dashboardga yo'naltirish
        xodim = Xodim.objects.first()

    boshlanish = request.GET.get('boshlanish')
    tugash = request.GET.get('tugash')

    ishlar = IshKuni.objects.filter(xodim=xodim).select_related('mahsulot').order_by('-sana')

    if boshlanish and tugash:
        ishlar = ishlar.filter(sana__range=[boshlanish, tugash])

    jami_soni = sum(i.soni for i in ishlar)
    jami_maosh = sum(i.mahsulot.narxi * i.soni for i in ishlar)

    return render(request, "kabinet.html", {
        "xodim": xodim,
        "ishlar": ishlar,
        "jami_soni": jami_soni,
        "jami_maosh": jami_maosh,
        "boshlanish": boshlanish,
        "tugash": tugash
    })


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
                ishga_kirilgan_sana=ishga_kirilgan_sana if ishga_kirilgan_sana else None,
                is_approved=True  # Admin qo'shgan xodim avtomatik tasdiqlangan bo'ladi
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

    if boshlanish and tugash:
        ishlar = ishlar.filter(sana__range=[boshlanish, tugash])

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
    pending_xodimlar = Xodim.objects.filter(is_approved=False)
    barcha_xodimlar = Xodim.objects.select_related('user').all().order_by('-id')

    return render(request, 'ish/admin_dashboard.html', {
        'xodimlar_soni': xodimlar_soni,
        'mahsulotlar_soni': mahsulotlar_soni,
        'ishlar_soni': ishlar_soni,
        'jami_tikilgan': jami_tikilgan,
        'pending_xodimlar': pending_xodimlar,
        'barcha_xodimlar': barcha_xodimlar,
    })

@user_passes_test(is_admin)
def approve_xodim(request, xodim_id):
    xodim = get_object_or_404(Xodim, id=xodim_id)
    xodim.is_approved = True
    xodim.save()
    messages.success(request, f"{xodim.ism} {xodim.familiya} tasdiqlandi!")
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def disapprove_xodim(request, xodim_id):
    xodim = get_object_or_404(Xodim, id=xodim_id)
    xodim.is_approved = False
    xodim.save()
    messages.warning(request, f"{xodim.ism} {xodim.familiya} tasdiqdan chiqarildi!")
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def toggle_xodim_status(request, xodim_id):
    xodim = get_object_or_404(Xodim, id=xodim_id)
    if xodim.user:
        xodim.user.is_active = not xodim.user.is_active
        xodim.user.save()
        status_text = "faollashtirildi" if xodim.user.is_active else "bloklandi"
        messages.info(request, f"{xodim.ism} {xodim.familiya} akkaunti {status_text}!")
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def manage_xodim_account(request, xodim_id):
    xodim = get_object_or_404(Xodim, id=xodim_id)
    if request.method == "POST":
        new_username = request.POST.get("username")
        new_password = request.POST.get("password")

        if xodim.user:
            if new_username and new_username != xodim.user.username:
                if User.objects.filter(username=new_username).exclude(id=xodim.user.id).exists():
                    messages.error(request, "Ushbu username band!")
                    return redirect('admin_dashboard')
                xodim.user.username = new_username

            if new_password:
                xodim.user.set_password(new_password)

            xodim.user.save()
            messages.success(request, f"{xodim.ism} {xodim.familiya} login ma'lumotlari yangilandi!")
        else:
            # Yangi user yaratib bog'lash
            if User.objects.filter(username=new_username).exists():
                messages.error(request, "Ushbu username band!")
                return redirect('admin_dashboard')

            user = User.objects.create_user(
                username=new_username,
                password=new_password,
                first_name=xodim.ism,
                last_name=xodim.familiya
            )
            xodim.user = user
            xodim.is_approved = True
            xodim.save()
            messages.success(request, f"{xodim.ism} {xodim.familiya} uchun yangi akkaunt yaratildi va bog'landi!")

    return redirect('admin_dashboard')



