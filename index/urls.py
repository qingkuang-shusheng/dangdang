#/user/author/yuandongbo
from django.urls import path, re_path
from index import views

app_name = 'index'

urlpatterns = [
    path('index/',views.index,name = 'index'),
    path('book_information/',views.book_information,name = 'book_information'),
    path('book_list/',views.book_list,name = 'book_list')
]