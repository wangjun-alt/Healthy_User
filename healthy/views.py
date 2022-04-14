import os
from django.http import HttpResponse, JsonResponse
import datetime
import json
import requests
from requests import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from healthy.models import *
from module.auth import GetOpenid
from module.dishfound import discern
from module.jwt_auth import create_token
from module.userinfo import GetUserAge, GetUserBMI
from module.sportdaychange import Sport_daychange

class LoginView(APIView):
    def post(self, request):
        """
            拿用户openid，微信小程序登录
            :return: response [fail or succees]
            response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
        """
        response = {"code": 200, "status": "fail", "errMsg": "", "data": ""}
        body = json.loads(request.body)
        nickname = body.get("Nick_Name")
        code = body.get("code")
        # code = request.data.get('code')
        reqUrl = "https://api.weixin.qq.com/sns/jscode2session?appid=wxffa946aa7b91fe34&secret=ffa3fe7508daa2b512809578d168f156&js_code=" + code + "&grant_type=authorization_code"
        identityInfo = requests.get(reqUrl).json()  # 向微信接口申请openId
        openid = identityInfo['openid'] if 'openid' in identityInfo else None
        # session_key = res['session_key'] if 'session_key' in res else None
        if not openid:
            return Response({'message': '微信调用失败'})
        try:
            user = Userinfo.objects.get(Open_Id=openid)
        except Userinfo.DoesNotExist:
            user = None
        if user and user.User_Target != None:
            user = Userinfo.objects.get(Open_Id=openid)
            response["code"] = 200
        else:
            user = Userinfo.objects.create(
                Open_Id=openid,
                Nick_Name=nickname,
            )
            response["code"] = 201
        token = create_token({'id': user.id, 'username': user.Open_Id})
        now_time = datetime.datetime.now()
        if user.Last_Time == None:
            user.Last_Time = now_time
        else:
            lasttime = user.Last_Time
            if int(now_time.year) > int(lasttime[0:4]) or int(now_time.month) > int(lasttime[5:7]) or int(now_time.day) > int(lasttime[8:10]):
                Sport_daychange(openid)
                if user.User_Target != None:
                    if user.User_Target == 0:
                        user.User_Consume = user.User_Metabolism - 150
                    elif user.User_Target == 1:
                        user.User_Consume = user.User_Metabolism - 500
                    else:
                        user.User_Consume = user.User_Metabolism - 1.5 * user.User_Weight * 4
                else:
                    response["code"] = 201
        response["data"] = token
        response["status"] = "succeed"
        return Response(data=response)


class Userinfosave(APIView):
    """
        计算并且保存用户信息，带参数访问
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """
    def post(self, request):
        response = {"code": 200, "status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        User_Height = request_data.get('User_Height')
        User_Weight = request_data.get('User_Weight')
        User_Gender = request_data.get('User_Gender')
        User_Borntime = request_data.get('User_Borntime')
        info = Userinfo.objects.get(Open_Id=openid)
        try:
            weight = WeightInfo.objects.get(Open_Id=openid)
        except WeightInfo.DoesNotExist:
            weight = None
        if weight:
            weight_heistory = WeightInfo.objects.get(Open_Id=openid)
        else:
            weight_heistory = WeightInfo.objects.create(Open_Id=openid)
        info.User_Weight = float(User_Weight)
        print(info.User_Weight)
        weight_heistory.User_Weight_One = info.User_Weight
        info.User_Borntime = User_Borntime
        info.User_Height = float(User_Height)
        info.User_Weight = float(User_Weight)
        info.User_Gender = User_Gender
        info.User_Age = int(GetUserAge(info.User_Borntime))
        info.User_BMI = float(GetUserBMI(User_Weight, User_Height))
        if User_Gender == '男':
            info.User_Bfp = ((1.2 * info.User_BMI) + (0.23 * info.User_Age) - 5.4 - (10.8 * 1)) / 100
        else:
            info.User_Bfp = ((1.2 * info.User_BMI) + (0.23 * info.User_Age) - 5.4 - (10.8 * 0)) / 100

        if User_Gender == '男':
            info.User_Metabolism = 66 + (13.7 * info.User_Weight) + (5.0 * info.User_Height) - (6.8 * info.User_Age)
        else:
            info.User_Metabolism = 665 + (9.6 * info.User_Weight) + (1.8 * info.User_Height) - (4.7 * info.User_Age)

        response["data"] = {
            "User_BMI": info.User_BMI,
            "User_Bfp": info.User_Bfp,
            "User_Metabolism": info.User_Metabolism,
            "User_Consume": info.User_Consume,
            "User_Residualheat": info.User_Residualheat,
            "User_Contend": info.User_Contend
        }
        response["status"] = "succeed"
        info.save()
        weight_heistory.save()
        return Response(data=response)


class Usersportlike(APIView):
    """
        对于用户想选择的运动进行保存，方便后期推送运动类型
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """
    def post(self, request):
        response = {"code": 200, "status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        User_Target = request_data.get('User_Target')
        SportLike_one = request_data.get('SportLike_one')
        SportLike_two = request_data.get('SportLike_two')
        SportLike_three = request_data.get('SportLike_three')
        SportLike_four = request_data.get('SportLike_four')
        SportLike_five = request_data.get('SportLike_five')
        SportLike_six = request_data.get('SportLike_six')
        token = request.headers.get('token')
        openid = GetOpenid(token)
        info = UserSportLike.objects.get(Open_Id=openid)
        user = Userinfo.objects.get(Open_Id=openid)
        user.User_Target = User_Target
        if user.User_Target == 0:
            user.User_Consume = user.User_Metabolism - 150
        else:
            if user.User_Target == 1:
                user.User_Consume = user.User_Metabolism - 500
            else:
                user.User_Consume = user.User_Metabolism - 1.5 * user.User_Weight * 4
        info.SportLike_one = SportLike_one
        info.SportLike_two = SportLike_two
        info.SportLike_three = SportLike_three
        info.SportLike_four = SportLike_four
        info.SportLike_five = SportLike_five
        info.SportLike_six = SportLike_six
        user.save()
        info.save()
        response["data"] = "保存成功"
        response["status"] = "succeed"
        return Response(data=response)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Userdishfound(APIView):
    """
        对用户上传的菜品图片进行识别并返回相关信息
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        token = request.headers.get('token')
        openid = GetOpenid(token)
        response = {"code": 200, "status": "fail", "errMsg": "", "data": ""}
        file_obj = request.FILES.get('Image_File', None)
        print(file_obj)
        print(type(file_obj))
        file_path = os.path.join(BASE_DIR, 'media', file_obj.name)
        result = discern(file_path, file_obj)
        response["data"] = result
        response["status"] = "succeed"
        return Response(data=response)


class NoteAddView(APIView):
    """
        修改用户个性签名
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Contend = request_data.get("contend")
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "User_Contend": info.User_Contend
        }
        return Response(data=response)


class SportRun(APIView):
    """
        根据用户跑步时间和距离计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        Sport_Time = request_data.get("Sport_Time")
        Sport_Distance = request_data.get("Sport_Distance")
        try:
            run = Sport_Run.objects.get(Open_Id=openid)
        except Sport_Run.DoesNotExist:
            run = None
        if run:
            runinfo = Sport_Run.objects.get(Open_Id=openid)
        else:
            runinfo = Sport_Run.objects.create(Open_Id=openid)
        runinfo.Run_Time = runinfo.Run_Time + Sport_Time
        info = Userinfo.objects.get(Open_Id=openid)
        Weight = info.User_Weight
        Run_Calorie = Weight * Sport_Time * (30 / (Sport_Time/(Sport_Distance/400)))
        runinfo.Run_Calorie = runinfo.Run_Calorie + Run_Calorie
        info.User_Consume = info.User_Consume - Run_Calorie
        info.save()
        runinfo.save()
        response['status'] = "succeed"
        response['data'] = {
            "Run_Calorie": Run_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class SportSwim(APIView):
    """
        根据用户根据用户游泳时间大概计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Sport_Time = request_data.get("Sport_Time")
        try:
            swim = Sport_Swim.objects.get(Open_Id=openid)
        except Sport_Swim.DoesNotExist:
            swim = None
        if swim:
            swiminfo = Sport_Swim.objects.get(Open_Id=openid)
        else:
            swiminfo = Sport_Swim.objects.create(Open_Id=openid)
        swiminfo.Swim_Time = swiminfo.Swim_Time + Sport_Time
        info = Userinfo.objects.get(Open_Id=openid)
        gender = info.User_Gender
        if gender == "男":
            Swim_Calorie = Sport_Time / 60 * 843
        else:
            Swim_Calorie = Sport_Time / 60 * 600
        swiminfo.Swim_Calorie = swiminfo.Swim_Calorie + Swim_Calorie
        info.User_Consume = info.User_Consume - Swim_Calorie
        info.save()
        swiminfo.save()
        response['status'] = "succeed"
        response['data'] = {
            "Swim_Calorie": Swim_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)

class SportCycling(APIView):
    """
        根据用户骑单车时间计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        Sport_Time = request_data.get("Sport_Time")
        Cycling_Calorie = Sport_Time / 60 * 480
        try:
            cycling = Sport_Cycling.objects.get(Open_Id=openid)
        except Sport_Cycling.DoesNotExist:
            cycling = None
        if cycling:
            cyclinginfo = Sport_Cycling.objects.get(Open_Id=openid)
        else:
            cyclinginfo = Sport_Cycling.objects.create(Open_Id=openid)
        cyclinginfo.Cycling_Time = cyclinginfo.Cycling_Time + Sport_Time
        cyclinginfo.Cycling_Calorie = cyclinginfo.Cycling_Calorie + Cycling_Calorie
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Cycling_Calorie
        info.save()
        cyclinginfo.save()
        response['status'] = "succeed"
        response['data'] = {
            "Cycling_Calorie": Cycling_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class SportBasketball(APIView):
    """
        根据用户骑单车时间计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        Sport_Time = request_data.get("Sport_Time")
        Basketball_Calorie = Sport_Time / 60 * 360
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Basketball_Calorie
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Basketball_Calorie": Basketball_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class Sportfootball(APIView):
    """
        根据用户踢足球时间计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Sport_Time = request_data.get("Sport_Time")
        Football_Calorie = Sport_Time / 60 * 450
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Football_Calorie
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Football_Calorie": Football_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)

class SportSkipping(APIView):
    """
        根据用户跳绳时间计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Sport_Time = request_data.get("Sport_Time")
        Skipping_Calorie = Sport_Time / 60 * 1200
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Skipping_Calorie
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Skipping_Calorie": Skipping_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class SportYoga(APIView):
    """
        根据用户瑜伽时间计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Sport_Time = request_data.get("Sport_Time")
        Yoga_Calorie = Sport_Time / 60 * 150
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Yoga_Calorie
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Yoga_Calorie": Yoga_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)



class SportAerobics(APIView):
    """
        根据用户健身操时间计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Sport_Time = request_data.get("Sport_Time")
        Aerobics_Calorie = Sport_Time / 60 * 1000
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Aerobics_Calorie
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Aerobics_Calorie": Aerobics_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class SportEllipsograph(APIView):
    """
        根据用户用椭圆仪的时长大概计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Sport_Time = request_data.get("Sport_Time")
        Ellipsograph_Calorie = Sport_Time / 60 * 1000
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Ellipsograph_Calorie
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Ellipsograph_Calorie": Ellipsograph_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class SportMountaineering(APIView):
    """
        根据用户使用登山机时长大概计算消耗卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Sport_Time = request_data.get("Sport_Time")
        Mountaineering_Calorie = Sport_Time / 60 * 1000
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Consume = info.User_Consume - Mountaineering_Calorie
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Mountaineering_Calorie": Mountaineering_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class UserIngestion(APIView):
    """
        根据用户使用的食物大概计算摄入卡路里
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """

    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        request_data = json.loads(request.body)
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        Dish_Name = request_data.get("Dish_Name")
        Dish_Weight = request_data.get("Dish_Weight")
        dish = Dish.objects.get(Dish_Name=Dish_Name)
        Ingestion_Calorie = float(Dish_Weight) * float(dish.Dish_Heat)
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Residualheat = float(info.User_Residualheat) + float(Ingestion_Calorie)
        if info.User_Residualheat > info.User_Metabolism:
            info.User_Consume = info.User_Consume + info.User_Residualheat - info.User_Metabolism
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "Ingestion_Calorie": Ingestion_Calorie,
            "User_Consume": info.User_Consume,
        }
        return Response(data=response)


class UserinfoGet(APIView):
    """
        获取用户的个人信息
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """
    def get(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        token = request.headers.get('token')
        openid = GetOpenid(token)
        # Sport_Name = request_data.get("Sport_Name")
        info = Userinfo.objects.get(Open_Id=openid)
        response['status'] = "succeed"
        response['data'] = {
            "Nick_Name": info.Nick_Name,
            "User_Age": info.User_Age,
            "User_Gender": info.User_Gender,
            "User_Height": info.User_Height,
            "User_Weight": info.User_Weight,
            "User_Borntime": info.User_Borntime,
            "User_BMI": info.User_BMI,
            "User_Bfp": info.User_Bfp,
            "User_Metabolism": info.User_Metabolism,
            "User_Consume": info.User_Consume,
            "User_Residualheat": info.User_Residualheat,
            "User_Contend": info.User_Contend,
        }
        return Response(data=response)


class UserinfoChange(APIView):
    """
        修改用户的身高和体重
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """
    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        token = request.headers.get('token')
        openid = GetOpenid(token)
        request_data = json.loads(request.body)
        User_Height = request_data.get("User_Height")
        User_weight = request_data.get("User_Weight")
        weight_history = WeightInfo.objects.get(Open_Id=openid)
        info = Userinfo.objects.get(Open_Id=openid)
        info.User_Height = User_Height
        info.User_Weight = User_weight
        if weight_history.User_Weight_Two == None:
            weight_history.User_Weight_Two = info.User_Weight
        else:
            if weight_history.User_Weight_Three == None:
                weight_history.User_Weight_Three = info.User_Weight
            else:
                if weight_history.User_Weight_Four == None:
                    weight_history.User_Weight_Four = info.User_Weight
                else:
                    if weight_history.User_Weight_Five == None:
                        weight_history.User_Weight_Five = info.User_Weight
                    else:
                        weight_history.User_Weight_One = weight_history.User_Weight_Two
                        weight_history.User_Weight_Two = weight_history.User_Weight_Three
                        weight_history.User_Weight_Three = weight_history.User_Weight_Four
                        weight_history.User_Weight_Four = weight_history.User_Weight_Five
                        weight_history.User_Weight_Five = info.User_Weight
        weight_history.save()
        info.save()
        response['status'] = "succeed"
        response['data'] = {
            "User_Height": info.User_Height,
            "User_Weight": info.User_Weight,
        }
        return Response(data=response)


class UserWeight(APIView):
    """
        体重日记
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """
    def get(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        token = request.headers.get('token')
        openid = GetOpenid(token)
        info = WeightInfo.objects.get(Open_Id=openid)
        one = info.User_Weight_One
        two = info.User_Weight_Two
        three = info.User_Weight_Three
        four = info.User_Weight_Four
        five = info.User_Weight_Five
        response['status'] = "succeed"
        response['data'] = {
            "User_Weight_One": one,
            "User_Weight_Two": two,
            "User_Weight_Three": three,
            "User_Weight_Four": four,
            "User_Weight_Five": five
        }
        return Response(data=response)

class SportinfoGet(APIView):
    """
        运动计划
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """
    def get(self, request):
        global one, one_time, one_calorie, two, two_time, two_calorie, three, three_time, three_calorie, percent
        response = {"status": "fail", "errMsg": "", "data": ""}
        token = request.headers.get('token')
        openid = GetOpenid(token)
        run = Sport_Run.objects.get(Open_Id=openid)
        swim = Sport_Swim.objects.get(Open_Id=openid)
        cycling = Sport_Cycling.objects.get(Open_Id=openid)
        user = Userinfo.objects.get(Open_Id=openid)
        if run.Sport_Mark == 1:
            one = run.Sport_Name
            one_time = run.Run_Time
            one_calorie = run.Run_Calorie
        elif swim.Sport_Mark == 1:
            two = swim.Sport_Name
            two_time = swim.Swim_Time
            two_calorie = swim.Swim_Calorie
        elif cycling.Sport_Mark == 1:
            three = cycling.Sport_Name
            three_time = cycling.Cycling_Time
            three_calorie = cycling.Cycling_Calorie
        elif user.User_Target == 0:
            percent = user.User_Sport_Heat / 150
        elif user.User_Target == 1:
            percent = user.User_Sport_Heat / 500
        elif user.User_Target == 2:
            percent = user.User_Sport_Heat / (1.5 * user.User_Weight * 4)
        response['status'] = "succeed"
        response['data'] = {
            "Sport_One_Name": one,
            "Sport_One_Time": one_time,
            "Sport_One_Calorie": one_calorie,
            "Sport_Two_Name": two,
            "Sport_Two_Time": two_time,
            "Sport_Two_Calorie": two_calorie,
            "Sport_Three_Name": three,
            "Sport_Three_Time": three_time,
            "Sport_Three_Calorie": three_calorie,
            "User_Sport_Time": user.User_Sport_Time,
            "User_Sport_Heat": user.User_Sport_Heat,
            "Percent": percent,
        }
        return Response(data=response)

class Feedback(APIView):
    """
        反馈与建议
        :return: response [fail or succees]
        response = {"code":200 "status": "fail", "errMsg": "", "data": ""}
    """
    def post(self, request):
        response = {"status": "fail", "errMsg": "", "data": ""}
        token = request.headers.get('token')
        openid = GetOpenid(token)
        request_data = json.loads(request.body)
        User_feedback = request_data.get("FeedBack")
        info = FeedBack.objects.get(Open_Id=openid)
        info.Feed_Name = User_feedback
        response['status'] = "succeed"
        response['data'] = "反馈成功"
        return Response(data=response)