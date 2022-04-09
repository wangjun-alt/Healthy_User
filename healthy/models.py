from django.db import models

class Userinfo(models.Model):
    """用户基本信息表"""
    Open_Id = models.CharField(max_length=100, verbose_name='openid', unique=True)
    Nick_Name = models.CharField(max_length=50, verbose_name='用户名', null=True, unique=False)
    User_Age = models.IntegerField(verbose_name='用户年龄', null=True, unique=False)
    User_Gender = models.CharField(max_length=10, verbose_name='用户性别', null=True, unique=False)
    User_Height = models.FloatField(verbose_name='身高', null=True, unique=False)
    User_Weight = models.FloatField(verbose_name='体重', null=True, unique=False)
    User_Borntime = models.DateTimeField(verbose_name='用户出生日期', null=True, unique=False)
    User_BMI = models.FloatField(verbose_name='BMI', null=True, unique=False)  # BMI
    User_Bfp = models.FloatField(verbose_name='体脂率', null=True, unique=False)  # 体脂率
    User_Metabolism = models.FloatField(verbose_name='每日基础代谢卡路里', null=True, unique=False)  # 基础代谢卡路里
    User_Consume = models.FloatField(verbose_name='每日待消耗热量', null=True, unique=False, default=0)  # 待消耗热量
    User_Residualheat = models.FloatField(verbose_name='当天摄入的卡路里', null=True, unique=False, default=0)  # 用户当天实时摄入热量
    User_Contend = models.CharField(max_length=100, verbose_name='个性标签', null=True, unique=False, default='该用户很懒，还没有发表任何简介')  # 用户个人简介
    User_Target = models.IntegerField(verbose_name="用户目的", null=True, unique=False, default=0)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Open_Id

    class Meta:
        verbose_name = "用户的基本信息"

class UserSportLike(models.Model):
    """用户感兴趣的运动"""
    Open_Id = models.CharField(max_length=100, verbose_name='openid', null=True)  # 用户标识符
    Nick_Name = models.CharField(max_length=50, verbose_name='用户名', null=True)
    SportLike_one = models.CharField(max_length=20, verbose_name='运动名称', null=True)
    SportLike_two = models.CharField(max_length=20, verbose_name='运动名称', null=True)
    SportLike_three = models.CharField(max_length=20, verbose_name='运动名称', null=True)
    SportLike_four = models.CharField(max_length=20, verbose_name='运动名称', null=True)
    SportLike_five = models.CharField(max_length=20, verbose_name='运动名称', null=True)
    SportLike_six = models.CharField(max_length=20, verbose_name='运动名称', null=True)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Nick_Name

    class Meta:
        verbose_name = '用户感兴趣的运动信息'
        verbose_name_plural = '用户感兴趣的运动信息'


class Dish(models.Model):
    """菜品信息表"""
    Dish_Name = models.CharField(max_length=20, verbose_name='菜品名称')
    Dish_Heat = models.FloatField(verbose_name='热量')  # 热量
    Dish_Carbohydrate = models.FloatField(verbose_name='碳水化合物含量', null=True, unique=False)  # 碳水化合物含量
    Dish_Protein = models.FloatField(verbose_name='蛋白质含量', null=True, unique=False)  # 蛋白质含量
    Dish_Fat = models.FloatField(verbose_name='脂肪含量', null=True, unique=False)  # 脂肪含量
    Dish_Cholesterol = models.FloatField(verbose_name='胆固醇含量', null=True, unique=False)  # 胆固醇含量
    Dish_Mineral = models.FloatField(verbose_name='矿物质含量', null=True, unique=False)  # 矿物质含量
    Dish_Carotene = models.FloatField(verbose_name='胡萝卜素含量', null=True, unique=False)  # 胡萝卜素含量
    Dish_Vitamin_A = models.FloatField(verbose_name='维生素A含量', null=True, unique=False)  # 维生素A含量
    Dish_Vitamin_C = models.FloatField(verbose_name='维生素C含量', null=True, unique=False)  # 维生素A含量
    Dish_Vitamin_E = models.FloatField(verbose_name='维生素E含量', null=True, unique=False)  # 维生素A含量
    Dish_Vitamin_B1 = models.FloatField(verbose_name='维生素B1含量', null=True, unique=False)  # 维生素A含量
    Dish_Vitamin_B2 = models.FloatField(verbose_name='维生素B2含量', null=True, unique=False)  # 维生素A含量
    Dish_Dietary = models.FloatField(verbose_name='膳食纤维', null=True, unique=False)  # 膳食纤维
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Dish_Name

    class Meta:
        verbose_name = '菜品基本信息'
        verbose_name_plural = '菜品基本信息'



class Sport(models.Model):
    """运动信息表"""
    Sport_Name = models.CharField(max_length=20, verbose_name='运动名称')
    Sport_Time = models.FloatField(verbose_name='运动时间', null=True, blank=True, default=0)
    Sport_Times = models.IntegerField(verbose_name='运动次数', null=True, blank=True, default=0)
    Sport_Distance = models.FloatField(verbose_name='运动里程', null=True, blank=True, default=0)
    Sport_Consume = models.FloatField(verbose_name='单位消耗', null=True, blank=True, default=0)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Sport_Name

    class Meta:
        verbose_name = '日常运动基本信息'
        verbose_name_plural = '日常运动基本信息'
