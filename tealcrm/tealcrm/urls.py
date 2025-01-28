
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from core.views import index,about
from django.conf import settings
from django.conf.urls.static import static
from userprofile.forms import LoginForm, SignupForm

urlpatterns = [
    path('',index, name='index' ),
    path('dashboard/leads/',include('leads.urls') ),
    path('dashboard/clients/',include('client.urls') ),
    path('dashboard/team/',include('team.urls') ),
    path('dashboard/',include('userprofile.urls') ),
    path('dashboard/',include('dashboard.urls') ),
    path('about/',about, name='about' ),
    path('login/',views.LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
