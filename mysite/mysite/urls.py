from django.contrib import admin
from django.urls import include, path
from umiz import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
]
