from django.urls import path
from . import views

urlpatterns=[
    path('bitcoin', views.bitcoin, name='bitcoin'),
    path('ethereum', views.ethereum, name='ethereum'),
]