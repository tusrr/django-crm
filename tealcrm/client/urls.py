from django.urls import path
from . import views

app_name='clients'

urlpatterns = [
    path('',views.clients_list,name='list'),
    path('<int:pk>/', views.clients_detail, name='detail'),
    path('add-client/', views.clients_add, name='add'),
    path('<int:pk>/edit/', views.clients_edit, name='edit'),
    path('<int:pk>/delete/', views.client_delete, name='delete'),

]
