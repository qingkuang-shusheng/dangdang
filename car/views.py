from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from car.models import Book, Car
from user import models
from user.models import TBook, TCar, TUser, TAddress


# Create your views here.
def car(request):
    txtUsername = request.session.get('txtUsername')
    # 登录

    if txtUsername:
        car = request.session.get('car')
        user = TUser.objects.get(user_name=txtUsername)
        user_car = TCar.objects.filter(id=user.user_id)
        # 外面有车
        if car:

            if request.session.get('car'):

                for book in car.book_list:
                    flag = False
                    for user_book in user_car:
                        if int(book.id) == user_book.book_id:
                            try:
                                with transaction.atomic():
                                    if int(user_book.goods_number) > int(book.count):
                                        pass
                                    else:
                                        user_book.goods_number = int(book.count)
                                    user_book.save()
                                    flag = True
                            except:
                                print('update error')
                    if not flag:
                        try:
                            with transaction.atomic():
                                TCar.objects.create(book_id=book.id, goods_number=book.count, id=user)
                        except:
                            print('insert1 error')
            else:

                for book in car.book_list:
                    try:
                        with transaction.atomic():
                            TCar.objects.create(book_id=book.id, goods_number=book.count, id=user)
                    except:
                        print('insert2 error')

            for user_book in user_car:
                flag = False
                for book in car.book_list:
                    if int(book.id) == user_book.book_id:
                        book.count = int(user_book.goods_number)
                        flag = True
                if not flag:
                    car.add(user_book.book_id, user_book.goods_number)

            request.session['car'] = car
            sum_price = 0
            sum_count = 0
            for i in car.book_list:
                sum_price = sum_price + float(i.price) * int(i.count)
                sum_count = sum_count + int(i.count)

            return render(request, 'dangdang/car.html',
                          {'txtUsername': txtUsername, 'car': car, 'sum_price': sum_price, 'sum_count': sum_count})
        else:
            car = Car()
            for user_book in user_car:
                print(user_book.book_id, user_book.goods_number)
                car.add(user_book.book_id, user_book.goods_number)

            print(car)
            request.session['car'] = car

            sum_price = 0
            sum_count = 0
            for i in car.book_list:
                sum_price = sum_price + float(i.price) * int(i.count)
                sum_count = sum_count + int(i.count)

            return render(request, 'dangdang/car.html',
                          {'car': car, 'sum_price': sum_price, 'sum_count': sum_count, 'txtUsername': txtUsername})

    elif request.session.get('car'):
        car = request.session.get('car')
        sum_price = 0
        sum_count = 0
        for i in car.book_list:
            sum_price += i.price * i.count
            sum_count += i.count

        return render(request, 'dangdang/car.html', {'car': car, 'sum_price': sum_price, 'sum_count': sum_count})
    # 未登录 外面无车
    else:
        car = request.session.get('car')
        return render(request, 'dangdang/car.html',{'car': car})


def add_car(request):
    book_id = request.POST.get('book_id')
    book_count = int(request.POST.get('book_count'))
    print('add_car', book_count)
    print('add_car', book_id)
    # 字典方式存储book
    # book_list= []
    # book_list.append({"id":book_id})
    # request.session['car'] = book_list
    car = request.session.get('car')
    txtUsername = request.session.get('txtUsername')

    if txtUsername:
        user = TUser.objects.get(user_name=txtUsername)
        user_car = TCar.objects.filter(id=user.user_id)
        for user_book in user_car:
            if int(book_id) == user_book.book_id:
                try:
                    user_book.goods_number = int(user_book.goods_number) + book_count
                    user_book.save()
                    print(user_book.goods_number)
                except:
                    print('update error')
    if car:
        car.add(book_id, book_count)
        request.session['car'] = car
        for res in car.book_list:
            print(res.id, res.name, res.count, res.price, res.picture)
    else:
        car = Car()
        car.add(book_id, book_count)
        request.session['car'] = car
        for res in car.book_list:
            print(res.id, res.name, res.count, res.price, res.picture)
    return HttpResponse('添加成功')


def remove_car(request):
    txtUsername = request.session.get('txtUsername')
    if txtUsername:
        user = TUser.objects.get(user_name=txtUsername)
        TCar.objects.filter(id=user.user_id).delete()
    book_name = request.POST.get('book_name')
    car = request.session.get('car')
    for i in car.book_list:
        if i.name == book_name:
            car.remove_book(i.id)

            request.session['car'] = car
            for i in car.book_list:
                print(i.name)
            return HttpResponse('删除成功')


def all_remove(request):
    car = request.session.get('car')
    print(car)
    car.clear()
    request.session.flush()
    print(request.session.get('car'))
    return HttpResponse('删除成功')


def indent(request):
    if request.GET.get('sum_price'):
        sum_price = round(float(request.GET.get('sum_price')),2)
    else:
        sum_price = 0
    new_sum_price = 0
    if request.session.get('txtUsername'):
        txtUsername = request.session.get('txtUsername')
        user = TUser.objects.get(user_name=txtUsername)

        # 订单里的图书信息
        user_books = TCar.objects.filter(id=user)
        res = TBook.objects.none()
        count_list = []
        price_list = []

        for user_book in user_books:
            book = TBook.objects.filter(book_id=user_book.book_id)
            new_sum_price += int(user_book.goods_number) * book[0].dangdang_price
            count_list.append(user_book.goods_number)
            price_list.append(int(user_book.goods_number) * book[0].dangdang_price)
            res |= book

        if new_sum_price > sum_price:
            sum_price = new_sum_price

        count_list.reverse()
        price_list.reverse()

        if txtUsername and TAddress.objects.filter(user_id=user):
            address_list = TAddress.objects.filter(user_id=user)
            return render(request, 'dangdang/indent.html',
                          {'price_list': price_list, 'count_list': count_list, 'res': res, 'address_list': address_list,
                           'txtUsername': txtUsername, 'sum_price': sum_price})
        elif txtUsername:
            return render(request, 'dangdang/indent.html',
                          {'price_list': price_list, 'count_list': count_list, 'res': res, 'txtUsername': txtUsername,
                           'sum_price': sum_price})
    return render(request, 'dangdang/indent.html')

