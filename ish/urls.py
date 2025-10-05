from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("xodimlar/", views.xodimlar, name="xodimlar"),
    path("mahsulotlar/", views.mahsulotlar, name="mahsulotlar"),
    path("ish-kunlari/", views.ish_kunlari, name="ish_kunlari"),
    path("hisobot/", views.hisobot, name="hisobot"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
