
from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index,name='login'),
    path('login/',views.loginUser,name='login'),
    path('registration/',views.register,name='register'),
    path('verify/',views.verify,name='verify'),
    path('check/<int:money>',views.check,name='check'),
    path('money/',views.money,name='money'),
    path('logout/',views.logoutUser,name='logout'),
    path('main/',views.main,name='main'),
    path('fraud/',views.fraud,name='fraud'),
]