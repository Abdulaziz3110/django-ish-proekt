from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("xodimlar/", views.xodimlar, name="xodimlar"),
    path("mahsulotlar/", views.mahsulotlar, name="mahsulotlar"),
    path("ish-kunlari/", views.ish_kunlari, name="ish_kunlari"),
    path("hisobot/", views.hisobot, name="hisobot"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("kabinet/", views.kabinet_view, name="kabinet"),
    path("approve-xodim/<int:xodim_id>/", views.approve_xodim, name="approve_xodim"),
    path("disapprove-xodim/<int:xodim_id>/", views.disapprove_xodim, name="disapprove_xodim"),
    path("toggle-xodim-status/<int:xodim_id>/", views.toggle_xodim_status, name="toggle_xodim_status"),
    path("manage-xodim-account/<int:xodim_id>/", views.manage_xodim_account, name="manage_xodim_account"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)