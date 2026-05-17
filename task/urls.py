from django.urls import path
from django.contrib.auth import views as auth_views
from task import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='task/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard_list'),
    path('dashboard/<slug:slug>/', views.dashboard_view, name='dashboard_detail'),
    # path('r/<slug:slug>/', views.redirect_and_track, name='redirect_and_track'),
    path('<slug:slug>/', views.redirect_url, name='redirect_url'),
]
