from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    '''列表页属性'''

    list_display = ['pk', 'Open_Id', 'Nick_Name', 'User_Age', 'User_Gender', 'User_Height', 'User_Weight',
                    'User_Borntime', 'User_BMI', 'User_Bfp', 'User_Metabolism', 'User_Consume', 'User_Residualheat',
                    'User_Contend', 'User_Target', 'Last_Time', 'User_Sport_Time', 'User_Sport_Heat', 'isDelete']
    list_filter = ['Open_Id', 'Nick_Name', 'User_Gender']  # 过滤字段
    search_fields = ['Nick_Name']  # 搜索字段
    list_per_page = 5

    '''添加、修改页属性'''
    # fields = []  # 属性的先后顺序
    # fieldsets = []  # 给属性分组

class DishAdmin(admin.ModelAdmin):
    list_display = ['pk', 'Dish_Name', 'Dish_Heat', 'Dish_Carbohydrate', 'Dish_Protein', 'Dish_Fat', 'Dish_Cholesterol',
                    'Dish_Mineral', 'Dish_Carotene', 'Dish_Vitamin_A', 'Dish_Vitamin_C', 'Dish_Vitamin_E',
                    'Dish_Vitamin_B1', 'Dish_Vitamin_B2', 'Dish_Dietary', 'isDelete']
    list_filter = ['Dish_Name']  # 过滤字段
    search_fields = ['Dish_Name']  # 搜索字段
    list_per_page = 5

class Sportadmin(admin.ModelAdmin):
    list_display = ['pk', 'Sport_Name', 'Sport_Time', 'Sport_Times', 'Sport_Distance', 'Sport_Consume', 'isDelete']
    list_filter = ['Sport_Name']  # 过滤字段
    search_fields = ['Sport_Name']  # 搜索字段
    list_per_page = 5

class SportLike(admin.ModelAdmin):
    list_display = ['pk', 'Open_Id', 'Nick_Name', 'SportLike_one', 'SportLike_two', 'SportLike_three', 'SportLike_four',
                    'SportLike_five', 'SportLike_six', 'isDelete']
    list_filter = ['Open_Id', 'Nick_Name']  # 过滤字段
    search_fields = ['Nick_Name']  # 搜索字段
    list_per_page = 5

class Weight(admin.ModelAdmin):
    list_display = ['pk', 'Open_Id', 'Nick_Name', 'User_Weight_One', 'User_Weight_Two', 'User_Weight_Three', 'User_Weight_Four',
                    'User_Weight_Five', 'isDelete']
    list_filter = ['Open_Id', 'Nick_Name']  # 过滤字段
    search_fields = ['Nick_Name']  # 搜索字段
    list_per_page = 5

'''注册表单'''
admin.site.register(Userinfo, UserAdmin)
admin.site.register(Sport, Sportadmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(UserSportLike, SportLike)
admin.site.register(WeightInfo, Weight)