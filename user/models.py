# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)
    cellphone = models.CharField(max_length=20, blank=True, null=True)
    post_code = models.CharField(max_length=6, blank=True, null=True)
    telephone = models.CharField(max_length=11, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 't_address'


class TCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_category'


class TBook(models.Model):
    book_id = models.IntegerField(primary_key=True)
    category = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)
    book_name = models.CharField(max_length=20, blank=True, null=True)
    book_description = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=60, blank=True, null=True)
    author_information = models.CharField(max_length=200, blank=True, null=True)
    dangdang_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    editor = models.CharField(max_length=80, blank=True, null=True)
    press = models.CharField(max_length=40, blank=True, null=True)
    publication_time = models.DateTimeField(blank=True, null=True)
    book_image = models.CharField(max_length=50, blank=True, null=True)
    sales = models.CharField(max_length=20, blank=True, null=True)
    inventory = models.CharField(max_length=20, blank=True, null=True)
    discount = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    comment = models.IntegerField(blank=True, null=True)
    book_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    page_number = models.IntegerField(blank=True, null=True)
    words = models.IntegerField(blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    print_time = models.DateTimeField(blank=True, null=True)
    impression = models.IntegerField(blank=True, null=True)
    sponsor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_discount(self):
        return "%.2f" % (int(self.dangdang_price) / int(self.book_price)*10)

    class Meta:
        db_table = 't_book'


class TCar(models.Model):
    car_id = models.AutoField(primary_key=True)
    id = models.ForeignKey('TUser', models.DO_NOTHING, db_column='id', blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    goods_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 't_car'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 't_order'


class TOrderItem(models.Model):
    order_item_id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    id = models.ForeignKey(TOrder, models.DO_NOTHING, db_column='id', blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_order_item'


class TUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    cell_number = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        db_table = 't_user'
