#/user/author/yuandongbo
from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('add_address/',views.add_address,name = 'add_address'),
    path('read_address/',views.read_address,name = 'read_address'),
    path('add_order_item/',views.add_order_item,name = 'add_order_item'),
    path('indent_ok/',views.indent_ok,name = 'indent_ok'),

]