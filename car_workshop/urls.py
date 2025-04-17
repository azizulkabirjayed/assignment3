from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointment/', views.appointment, name='appointment'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_view/', views.admin_view, name='admin_view'),

]