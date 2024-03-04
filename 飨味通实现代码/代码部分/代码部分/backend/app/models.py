# Create your models here.
from django.db import models
from django.core.validators import MaxLengthValidator
from .util import *

ID_LEN = 8
PHONE_LEN = 11
TEXT_LEN = 20
NUM_DIG = 5
CON_LEN = 500
SCALE_DIG = 3


class Picture(models.Model):
    Pid = models.CharField(max_length=ID_LEN, validators=[MaxLengthValidator(ID_LEN)], primary_key=True)
    path = models.ImageField(
        upload_to='image/',
        storage=ImageStorage(),
        verbose_name='图片路径',
        null=True
    )

    class Meta:
        db_table = 'Picture'
        verbose_name = '图片'
        verbose_name_plural = verbose_name


class User(models.Model):
    objects = models.Manager()
    Uid = models.CharField(max_length=ID_LEN, validators=[MaxLengthValidator(ID_LEN)], primary_key=True)
    Uname = models.CharField(max_length=TEXT_LEN, verbose_name='用户名')
    phone = models.CharField(max_length=PHONE_LEN, validators=[MaxLengthValidator(PHONE_LEN)], verbose_name='用户手机')
    pwd = models.CharField(max_length=TEXT_LEN, verbose_name='用户密码')
    Pid = models.ForeignKey(Picture, on_delete=models.CASCADE, verbose_name='用户头像')

    class Meta:
        db_table = 'User'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Group(models.Model):
    objects = models.Manager()
    Gid = models.CharField(max_length=ID_LEN, validators=[MaxLengthValidator(ID_LEN)], primary_key=True)
    Gname = models.CharField(max_length=TEXT_LEN, verbose_name='菜品组名')

    class Meta:
        db_table = 'Group'
        verbose_name = '菜品组'
        verbose_name_plural = verbose_name


class Dish(models.Model):
    objects = models.Manager()
    Did = models.CharField(max_length=ID_LEN, validators=[MaxLengthValidator(ID_LEN)], primary_key=True)
    Dname = models.CharField(max_length=TEXT_LEN, verbose_name='菜品名')
    price = models.DecimalField(max_digits=NUM_DIG, verbose_name='菜品价格', decimal_places=1)
    description = models.CharField(max_length=CON_LEN, verbose_name='菜品描述')
    score = models.DecimalField(max_digits=SCALE_DIG, verbose_name='菜品评分', decimal_places=2)
    star = models.DecimalField(max_digits=NUM_DIG, verbose_name='菜品收藏量', decimal_places=0)
    remain = models.DecimalField(max_digits=NUM_DIG, verbose_name='菜品剩余', decimal_places=0)
    Pid = models.ForeignKey(Picture, on_delete=models.CASCADE, verbose_name='菜品图片')
    Gid = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='菜品菜品组')

    class Meta:
        db_table = 'Dish'
        verbose_name = '菜品'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    objects = models.Manager()
    Cid = models.CharField(max_length=ID_LEN, validators=[MaxLengthValidator(ID_LEN)], primary_key=True)
    Uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论用户')
    Did = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='评论菜品', default='')
    content = models.CharField(max_length=CON_LEN, verbose_name='评论内容')
    score = models.DecimalField(max_digits=SCALE_DIG, decimal_places=2, verbose_name='评论评分')

    class Meta:
        db_table = 'Comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    objects = models.Manager()
    Tid = models.CharField(max_length=ID_LEN, validators=[MaxLengthValidator(ID_LEN)], primary_key=True)
    Tname = models.CharField(max_length=TEXT_LEN, verbose_name='标签名')

    class Meta:
        db_table = 'Tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Order(models.Model):
    objects = models.Manager()
    Oid = models.CharField(max_length=ID_LEN, validators=[MaxLengthValidator(ID_LEN)], primary_key=True)
    Uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='订单用户')
    total = models.DecimalField(max_digits=NUM_DIG, decimal_places=0, verbose_name='订单总价')
    time = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class DishTag(models.Model):
    objects = models.Manager()
    Did = models.ForeignKey(Dish, on_delete=models.CASCADE)
    Tid = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'DishTag'
        unique_together = (('Did', 'Tid'),)


class UserStarDish(models.Model):
    objects = models.Manager()
    Uid = models.ForeignKey(User, on_delete=models.CASCADE)
    Did = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UserStarDish'
        unique_together = (('Uid', 'Did'),)


class DishOrder(models.Model):
    objects = models.Manager()
    Oid = models.ForeignKey(Order, on_delete=models.CASCADE)
    Did = models.ForeignKey(Dish, on_delete=models.CASCADE)
    number = models.DecimalField(max_digits=NUM_DIG, decimal_places=0, verbose_name='点菜数量')

    class Meta:
        db_table = 'DishOrder'
        unique_together = (('Oid', 'Did'),)


class CommentPicture(models.Model):
    objects = models.Manager()
    Cid = models.ForeignKey(Comment, on_delete=models.CASCADE)
    Pid = models.ForeignKey(Picture, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CommentPicture'
        unique_together = (('Cid', 'Pid'),)


