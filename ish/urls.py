from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("", views.index, name="index"),
    path("xodimlar/", views.xodimlar, name="xodimlar"),
    path("mahsulotlar/", views.mahsulotlar, name="mahsulotlar"),
    path("ish-kunlari/", views.ish_kunlari, name="ish_kunlari"),
    path("hisobot/", views.hisobot, name="hisobot"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)