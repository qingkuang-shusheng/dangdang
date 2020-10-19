import random
import string
import time

from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from user.models import TAddress, TUser,TOrderItem,TOrder,TCar


# Create your views here.

def add_address(request):
    txtUsername = request.session.get('txtUsername')
    user = TUser.objects.get(user_name=txtUsername)
    ship_man = request.POST.get('ship_man')
    address = request.POST.get('address')
    postcode = request.POST.get('postcode')
    telephone = request.POST.get('telephone')
    phone = request.POST.get('phone')

    address_check = request.POST.get('address_check')
    postcode_check = request.POST.get('postcode_check')
    phone_check = request.POST.get('phone_check')
    telephone_check = request.POST.get('telephone_check')

    print(ship_man, address, postcode, telephone, phone, address_check, postcode_check, phone_check, telephone_check)

    address_list = TAddress.objects.filter(user_id=user.user_id)
    if ship_man and address_check and postcode_check and phone_check == 'true':
        for i in address_list:
            if i.name == ship_man and i.detail_address == address and i.cellphone == phone and postcode == i.post_code:
                return HttpResponse('重复phone')
        try:
            with transaction.atomic():
                TAddress.objects.create(user_id=user.user_id, post_code=postcode, cellphone=phone,
                                        detail_address=address, name=ship_man)
        except:
            print('插入phone失败')
        return HttpResponse('成功phone')

    elif ship_man and address_check and postcode_check and telephone_check == 'true':
        for i in address_list:
            if i.name == ship_man and i.detail_address == address and i.telephone == telephone and \
                    postcode == i.post_code:
                return HttpResponse('重复telephone')
        try:
            with transaction.atomic():
                TAddress.objects.create(user_id=user.user_id, telephone=telephone, post_code=postcode,
                                        detail_address=address, name=ship_man)
        except:
            print('插入telephone失败')
        return HttpResponse('成功telephone')

def add_order_item(request):
    re_address = request.POST.get('address')
    print('as',re_address)
    sum_price = request.POST.get('sum_price')
    print (sum_price)
    order_id = random.sample(string.digits,8)
    print(''.join(order_id))
    txtUsername = request.session.get('txtUsername')
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user = TUser.objects.get(user_name=txtUsername)
    user_car = TCar.objects.filter(id=user)
    address = TAddress.objects.get(detail_address=re_address)
    TOrder.objects.create(order_id=int(''.join(order_id)),create_time=date,price=sum_price,address_id=address.address_id,user_id=user.user_id)
    order = TOrder.objects.filter(user_id=user).order_by('id')

    query_order = order[order.count()-1]

    for user_book in user_car:
        TOrderItem.objects.create(book_id=user_book.book_id,count=user_book.goods_number,id=query_order)

    return HttpResponse('订单添加成功')

def read_address(request):
    address = request.POST.get('check')
    if address == '添加新地址':
        return HttpResponse('添加新地址')
    address_list = TAddress.objects.get(detail_address=address)
    data = {
        'name': address_list.name,
        'address': address_list.detail_address,
        'cellphone': address_list.cellphone,
        'telephone': address_list.telephone,
        'postcode': address_list.post_code,
    }

    def my(n):
        if n is None:
            return ' '

    return JsonResponse(data, safe=False, json_dumps_params={"default": my})

def indent_ok(request):
    txtUsername = request.session.get('txtUsername')
    user = TUser.objects.get(user_name=txtUsername)
    order = TOrder.objects.filter(user_id=user).order_by('id')

    query_order = order[order.count()-1]

    address = TAddress.objects.get(user_id=user)
    car = TCar.objects.filter(id=user)
    sum_count = 0
    for i in car:
        sum_count += int(i.goods_number)
    car.delete()
    del request.session['car']
    return render(request,'dangdang/indent ok.html',{'res':query_order,'address':address,'sum_count':sum_count})