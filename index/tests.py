import random

import django
from django.test import TestCase
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangdang.settings")
django.setup()
# Create your tests here.
from user.models import TBook
# book = TBook.objects.create(category_id=1,book_name='半小时漫画中国哲学',book_description='二混子新作！明明在看诸子百家掐架，看完却懂了中国哲学精华！）',author='陈磊.半小时漫画团队 '
#                             ,dangdang_price=35.90,press='江苏凤凰文艺出版社',comment=785)
# book = TBook.objects.create(book_name='一往无前 小米官方授权传记',book_description='首次完整揭秘小米独特商业模式，雷军演讲力荐阅读 开启副业赚钱，经管理财5折封顶点击>>',author='范海涛 '
#                             ,dangdang_price=58.00,press='中信出版社',comment=121)
# for i in range(20):
#     number = round(random.uniform(1,100),2)
#     TBook.objects.create(book_name='小米'+str(i),dangdang_price=number,book_image='book_image/一夜长大.png')
# for i in range(1,22):
#     number = random.randint(1,10000)
#     res = TBook.objects.get(book_id=i)
#     res.comment = number
#     res.save()
#
# for i in range(1,22):
#     number = round(random.uniform(1,100),2)
#     res = TBook.objects.get(book_id=i)
#     res.dangdang_price = number
#     res.save()
# for i in range(1,22):
#     number = round(random.uniform(100,150),2)
#     res = TBook.objects.get(book_id=i)
#     res.book_price = number
#     res.save()
# for i in range(1,22):
#     res = TBook.objects.get(book_id=i)
#     res.author = '雷军'
#     res.save()
# print(book)
# for i in range(1,22):
#     res = TBook.objects.get(book_id=i)
#     res.discount = res.dangdang_price/res.book_price*10
#     res.save()