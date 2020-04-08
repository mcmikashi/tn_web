from django.urls import path

from . import views

app_name = 'velopolitain'
urlpatterns = [
    path('', views.MainVelopolitain.as_view(), name='index'),
    path('b/<str:slug>', views.BlogVelopolitain.as_view(), name='lab'),
]
