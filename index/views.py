from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render
from user.models import TCategory, TBook


# import datetime

# Create your views here.
def index(request):
    # 主页左侧书籍目录分类功能块实现
    level1 = TCategory.objects.filter(level=1)
    level2 = TCategory.objects.filter(level=2)
    # 按出版时间实现新书上架榜模块功能
    publication_time = TBook.objects.order_by('-publication_time')
    pagtor = Paginator(publication_time.all(), per_page=8)
    page = pagtor.page(1)
    # 按评论数量实现主编推荐模块功能
    comment = TBook.objects.order_by('-comment')
    pagtor2 = Paginator(comment.all(), per_page=8)
    page2 = pagtor2.page(1)
    # 按出版日期和销售数量实现新书热卖榜功能
    res = TBook.objects.filter(publication_time__gte='2020-1-1 0:0:0').order_by('-sales')
    # print(res[0].publication_time.second,type(res[0].publication_time))
    pagtor3 = Paginator(res, per_page=5)
    page3 = pagtor3.page(1)

    content = {
        'level1': level1,
        'level2': level2,
        'page': page,
        'page2': page2,
        'page3': page3}
    #用户第一次登陆无cookie 必须用如下方法渲染欢迎用语 用户名会在url里暴露
    # if request.GET.get('txtUsername') :
    if request.session.get('txtUsername') :
        txtUsername = request.session.get('txtUsername')
        print(1,txtUsername)
        print('index',request.COOKIES)
        print('index', request.session.get('txtUsername'))
        content = {
            'level1': level1,
            'level2': level2,
            'page': page,
            'page2': page2,
            'page3': page3,
            'txtUsername': txtUsername,
        }
        return render(request, 'dangdang/index.html', content)
    # 若用户存在cookie时 不想在路径里显示用户名 设置如下方法
    elif request.COOKIES.get('txtUsername'):
        txtUsername = request.COOKIES.get('txtUsername')
        print(2,txtUsername)
        content = {
            'level1': level1,
            'level2': level2,
            'page': page,
            'page2': page2,
            'page3': page3,
            'txtUsername': txtUsername,
        }
        return render(request, 'dangdang/index.html', content)
    else:
        return render(request, 'dangdang/index.html', content)


def book_information(request):
    id = request.GET.get('page_id')
    res = TBook.objects.get(book_id=id)
    txtUsername = request.session.get('txtUsername')

    year = res.publication_time.year
    month = res.publication_time.month
    day = res.publication_time.day

    content = {
        'book_name': res.book_name,
        'book_description': res.book_description,
        'author': res.author,
        'dangdang_price': res.dangdang_price,
        'book_price': res.book_price,
        'comment': res.comment,
        'sales': res.sales,
        'year': year,
        'month': month,
        'day': day,
        'book_image': res.book_image,
        'press': res.press,
        'res':res,
        'txtUsername':txtUsername,
    }
    print('l',res.book_id)
    return render(request, 'dangdang/Book details.html', content)


# def book_list(request, page_id, cate_id, self_level):
def book_list(request):
    category_id = request.GET.get('category_id')
    level = request.GET.get('level')
    default_flag = request.GET.get('default_flag')
    sales_flag = request.GET.get('sales_flag')
    price_flag = request.GET.get('price_flag')
    time_flag = request.GET.get('time_flag')
    txtUsername = request.session.get('txtUsername')

    print(category_id, level,)

    Qs = []

    if level == '1':
        idList = []
        res = TCategory.objects.filter(parent_id=category_id)
        for i in res:
            idList.append(i.category_id)
        priorCategory = TBook.objects.filter(category_id__in=idList)
        if default_flag:
            priorCategory = priorCategory
        elif sales_flag:
            priorCategory = priorCategory.order_by('sales')
        elif price_flag:
            priorCategory = priorCategory.order_by('dangdang_price')
            print(priorCategory)
        elif time_flag:
            priorCategory = priorCategory.order_by('publication_time')
        Qs.append(priorCategory)
    elif level == '2':
        secondCategory = TBook.objects.filter(category_id=category_id)
        if default_flag:
            secondCategory = secondCategory
        elif sales_flag:
            secondCategory = secondCategory.order_by('sales')
        elif price_flag:
            secondCategory = secondCategory.order_by('dangdang_price')

        elif time_flag:
            secondCategory = secondCategory.order_by('publication_time')
        Qs.append(secondCategory)

    pagtor = Paginator(Qs[0],per_page = 2)

    page_id = request.GET.get('page_id',1)
    if int(page_id) > pagtor.num_pages :
        page_id = pagtor.num_pages
    elif  int(page_id) < 0:
        page_id = 1
    page = pagtor.page(page_id)

    return render(request, 'dangdang/booklist.html', {'default_flag':default_flag,'sales_flag':sales_flag,'price_flag':price_flag,'time_flag':time_flag,'res': page,'category_id':category_id,'level':level,'txtUsername':txtUsername})

