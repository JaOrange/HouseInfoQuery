from django.db import models

# Create your models here.(在这个文件里创建数据库中的表，表的名称就是：houseinfo_类名)
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)


class bjHouseInfo(models.Model):
    builder = models.CharField(max_length=256, verbose_name="开发商")
    houseType = models.CharField(max_length=64, verbose_name='户型')
    area = models.CharField(max_length=20, verbose_name='面积')
    direction = models.CharField(max_length=20, verbose_name='朝向')
    decoration = models.CharField(max_length=20, verbose_name='装修')
    floor = models.CharField(max_length=60, verbose_name='楼层')
    year = models.CharField(max_length=20, verbose_name='年份')
    structure = models.CharField(max_length=20, verbose_name='结构')
    total_price = models.CharField(max_length=20, verbose_name='售价(万元)')
    unit_price = models.CharField(max_length=20, verbose_name='单价(元/平方米)')