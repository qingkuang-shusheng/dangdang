#/user/author/yuandongbo
from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('register/',views.register,name = 'register'),
    path('register_name/',views.register_name,name = 'register_name'),
    path('register_password/',views.register_password,name = 'register_password'),
    path('get_vsCode/',views.get_vsCode,name = 'get_vsCode'),
    path('final_justify/',views.final_justify,name = 'final_justify'),
    path('register_logic/',views.register_logic,name = 'register_logic'),
    path('register_ok/',views.register_ok,name = 'register_ok'),
    path('login/',views.login,name = 'login'),
    path('login_logic/',views.login_logic,name = 'login_logic'),
    path('quit_login/',views.quit_login,name = 'quit_login')
]