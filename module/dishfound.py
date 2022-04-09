import os

from aip import AipImageClassify

from healthy.models import Dish

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def discern(file_path, file_obj):
    """ 你的 APPID AK SK """
    APP_ID = '24772730'
    API_KEY = 'SAx4BEE5KNjy5C70coBGjttw'
    SECRET_KEY = 'TjMHiD58XlxfxlKX512FYqf8eDsibnmG'
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    with open(file_path, 'rb') as fp:
        image = fp.read()

    """ 调用菜品识别 """
    # result = (client.dishDetect(image))

    """ 如果有可选参数 """
    options = {}
    options["top_num"] = 10
    options["filter_threshold"] = "0.7"
    options["baike_num"] = 1
    """ 带参数调用菜品识别 """
    result = client.dishDetect(image, options)
    print(result)
    result_one = result.get("result")
    result_two = result_one[0]
    logo = result_two.get('has_calorie')
    data = {}
    if logo == True:
        calorie = result_two.get('calorie')  # 每一百克所包含的食物卡路里
        dish_name = result_two.get('name')
        print(dish_name)
        try:
            info = Dish.objects.get(Dish_Name=dish_name)
            print(info)
        except Dish.DoesNotExist:
            info = None
        if info:
            info.Dish_Heat = calorie
            data = {
                "Dish_Name": info.Dish_Name,
                "Dish_Heat": info.Dish_Heat,
                "Dish_Protein": info.Dish_Protein,
                "Dish_Fat": info.Dish_Fat,
                "Dish_Carbohydrate": info.Dish_Carbohydrate,
                "Dish_Dietary": info.Dish_Dietary,
                "Dish_Vitamin_A": info.Dish_Vitamin_A,
                "Dish_Vitamin_C": info.Dish_Vitamin_C,
                "Dish_Vitamin_E": info.Dish_Vitamin_E,
                "Dish_Vitamin_B1": info.Dish_Vitamin_B1,
                "Dish_Vitamin_B2": info.Dish_Vitamin_B2,
                "Dish_Carotene": info.Dish_Carotene,
                "Dish_Cholesterol": info.Dish_Cholesterol,
                "Dish_Mineral": info.Dish_Mineral
            }
        else:
            dish = Dish.objects.create(
                Dish_Name=dish_name,
                Dish_Heat=calorie,
            )
            data = {
                "Dish_Name": dish.Dish_Name,
                "Dish_Heat": dish.Dish_Heat,
            }
        # 这里如果数据库也没有该食品信息，那么返回错误信息
    return data
