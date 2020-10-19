#/user/author/yuandongbo
from django.urls import path,include
from car import views

app_name = 'car'

urlpatterns = [
    path('car/',views.car,name='car'),
    path('add_car/',views.add_car,name='add_car'),
    path('remove_car/',views.remove_car,name='remove_car'),
    path('all_remove/',views.all_remove,name='all_remove'),
    path('indent/',views.indent,name='indent'),
]