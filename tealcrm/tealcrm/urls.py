
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from core.views import index,about
from userprofile.views import signup
urlpatterns = [
    path('',index, name='index' ),
    path('dashboard/',include('dashboard.urls') ),
    path('about/',about, name='about' ),
    path('signup/',signup, name='signup' ),
    path('login/',views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('admin/', admin.site.urls),
]
