from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path("",views.index,name='home'),
    path("startchain/",views.startchain,name='startchain'),
    path("chainprint/",views.chainprint,name='chainprint'),
    path("lock/",views.lock,name='lock'),
    path("unlock/",views.unlock,name='unlock'),
    path("reset/",views.reset,name='reset')
]
