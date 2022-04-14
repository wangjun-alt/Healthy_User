from healthy import views
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="接口文档平台",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),), public=True,
    permission_classes=(permissions.AllowAny,),)
urlpatterns = [
    path('user/register/', views.LoginView.as_view()),  # 用户登录，注册
    path('user/save/', views.Userinfosave.as_view()),  # 用户信息的保存
    path('user/sportlike/', views.Usersportlike.as_view()),  # 用户喜好运动的保存
    path('dish/found/', views.Userdishfound.as_view()),  # 对用户上传的菜品图片进行识别并返回相关信息
    path('revise/contend/', views.NoteAddView.as_view()),  # 修改用户个性签名
    path('sport/run/', views.SportRun.as_view()),  # 根据用户跑步时间和距离计算消耗卡路里
    path('sport/cycling/', views.SportCycling.as_view()),  # 根据用户骑单车时长大概计算消耗卡路里
    path('sport/basketball/', views.SportBasketball.as_view()),  # 根据用户打篮球时长大概计算消耗卡路里
    path('sport/skipping/', views.SportSkipping.as_view()),  # 根据用户跳绳时长大概计算消耗卡路里
    path('sport/yoga/', views.SportYoga.as_view()),  # 根据用户练瑜伽时长大概计算消耗卡路里
    path('sport/Aerobics/', views.SportAerobics.as_view()),  # 根据用户健身操时长大概计算消耗卡路里
    path('sport/ellipsograph/', views.SportEllipsograph.as_view()),  # 根据用户用椭圆仪的时长大概计算消耗卡路里
    path('sport/mountaineering/', views.SportMountaineering.as_view()),  # 根据用户使用登山机时长大概计算消耗卡路里
    path('dish/ingestion/', views.UserIngestion.as_view()),  # 根据用户使用的食物大概计算摄入卡路里
    path('user/info/', views.UserinfoGet.as_view()),  # 获取用户信息
    path('user/change/', views.UserinfoChange.as_view()),  # 用户信息主要是体重以及身高的更改
    path('user/weight/', views.UserWeight.as_view()),  # 体重计划
    path('sport/info/', views.SportinfoGet.as_view()),  # 运动计划
    path('user/feedback/', views.Feedback.as_view()),  # 反馈与建议
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # 接口文档接口
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # 接口文档接口
]