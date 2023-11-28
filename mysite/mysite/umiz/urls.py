from umiz import views
from django.urls import include, path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index),
    path('dashboard/',views.dashboardView, name='dashboard'),
    path('register/', views.RegisterView, name='register_url'),
    path('login/', LoginView.as_view(), name='login_url'),
]
