from django.urls import path
from django.contrib.auth import views as auth_views
from task import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='task/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('/dashboard/', views.dashboard_view, name='dashboard'),
    path('tester/', views.tester_view, name='tester'),
    path('demo/', views.demo_view, name='demo'),
    path('<slug:slug>/', views.redirect_url, name='redirect_url'),
]