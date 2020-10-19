from django.db import models
from user.models import TBook
# Create your models here.

class Book:
    def __init__(self, id, count=1):
        book = TBook.objects.get(book_id=id)
        self.id = id
        self.count = count
        self.price = book.dangdang_price
        self.name = book.book_name
        self.picture = book.book_image


class Car:
    def __init__(self):
        self.book_list = []  # 空列表

    def add(self, id, count=1):  # 将所选书籍加入购物车
        book = self.get_book(id,count)  # 判断所选书籍是否在购物车中
        if book:
            book.count += count  # 在的话数量加
        else:
            book = Book(id=id, count=count)  # 不在的话创造book对象
            self.book_list.append(book)  # 加入car类中的书籍列表

    def remove_book(self, id):
        book = self.get_book(id)  # 找到要删除书籍的对象   在购物车的书籍列表里删除
        self.book_list.remove(book)

    def get_book(self, id,count=1):
        for book in self.book_list:
            if book.id == id:  # 如果找到所选书籍存在购物车里的书籍列表里  返回当前book对象
                return book

    def clear(self):
        self.book_list = []