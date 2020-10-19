from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from user.models import TUser
from captcha.image import ImageCaptcha
import string, random


# Create your views here.

def register(request):
    source_url = request.GET.get('url')
    return render(request, 'dangdang/register.html',{'url':source_url})


def register_name(request):
    register_username = request.POST.get('register_username')
    # print(register_username)
    res = TUser.objects.filter(user_name=register_username)
    if res:
        return HttpResponse("用户名已存在")
    return HttpResponse('用户名可使用')


def register_password(request):
    register_password = request.POST.get('register_password')
    res = TUser.objects.filter(password=register_password)
    if res:
        return HttpResponse('')


def get_vsCode(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters + string.digits, 4)
    random_code = ''.join(code)
    data = image.generate(random_code)
    res = HttpResponse(data, "image/png")
    res.set_cookie('code',random_code)

    return res


def final_justify(request):
    COOKIES_code = request.COOKIES.get('code')
    register_username = request.POST.get('register_username')
    txt_password = request.POST.get('txt_password')
    current_code = request.POST.get('txt_code')

    res = TUser.objects.filter(user_name=register_username, password=txt_password)
    if not res:
        if current_code.lower() == COOKIES_code.lower():
            return HttpResponse("可注册")
    return HttpResponse('失败')

# if url == 'book_list':
#
#     reutrn redirect(reverse('带跳转的url', args=[page_id, cate_id, self_level]))

def register_logic(request):
    name = request.GET.get('name')
    password = request.GET.get('password')
    source_url = request.GET.get("url")
    category_id= request.GET.get("category_id")
    level= request.GET.get("level")

    if source_url and category_id and level:
        url = source_url + "&&category_id="+category_id +"&&level=" + level
        print('aaa',source_url)
    else:
        url = source_url
    print(name, password, url)

    with transaction.atomic():
        try:
            res = TUser.objects.create(user_name=name, password=password)
        except:
            print('error')

    request.session['txtUsername'] = name
    print ( request.session['txtUsername'] )
    return render(request,"dangdang/register ok.html",{"url":url})



def register_ok(request):
    # url = request.GET.get('url')
    # print(url)
    # txtUsername = request.GET.get('name')

    return render(request, 'dangdang/register ok.html')



def login(request):
    source_url = request.GET.get('url')
    page_id = request.GET.get('page_id')
    print(source_url,page_id)
    if request.COOKIES.get('txtUsername'):
        txtUsername = request.COOKIES.get('txtUsername')
        return redirect(reverse('index:index') + "?txtUsername=" + txtUsername)
    elif request.session.get('txtUsername'):
        return redirect(reverse('index:index'))
    return render(request, 'dangdang/login.html',{'source_url':source_url,'page_id':page_id})


def login_logic(request):
    #当前是用$('form').serliaze 传递ajax
    # print(request.POST.get('source_url'))
    #注释的是用拼接数据传递ajax

    current_code = request.POST.get('current_code')
    if current_code.lower() != request.COOKIES.get('code').lower():
        return HttpResponse("验证码错误")
    # txt_username = request.POST.get('txt_username')
    txtUsername = request.POST.get('txtUsername')
    txtPassword = request.POST.get('txtPassword')
    # check_token = request.POST.get('check')
    check_token = request.POST.get('autologin')

    #session保持登陆状态
    request.session['txtUsername'] = txtUsername

    # if TUser.objects.filter(user_name=txt_username, password=txtPassword):
    if TUser.objects.filter(user_name=txtUsername, password=txtPassword):
        res = HttpResponse("成功")
        if check_token:
            res.set_cookie("txtUsername", txtUsername, max_age=60 * 60 * 24 * 7)
        return res
    else:
        return HttpResponse("失败")


def quit_login(request):
    url = request.GET.get('url')
    category_id = request.GET.get('category_id')
    level = request.GET.get('level')
    print(url,category_id,level)
    if url and category_id and level:
        source_url = url + "&&category_id="+category_id +"&&level=" + level

    else:
        source_url = url
    txtUsername = request.COOKIES.get('txtUsername')
    res = redirect(source_url)
    res.set_cookie('txtUsername', txtUsername, max_age=0)
    request.session.flush()
    # del request.session['txtUsername']

    # print('quit',request.COOKIES)
    # print('quit',request.session.get('txtUsername'))
    return res
