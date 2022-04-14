from healthy.models import *

def Sport_daychange(openid):
    Run = Sport_Run.objects.get(Open_Id=openid)
    Swim = Sport_Swim.objects.get(Open_Id=openid)
    Cycling = Sport_Cycling.objects.get(Open_Id=openid)
    Cycling.Cycling_Time = 0
    Cycling.Cycling_Calorie = 0
    Swim.Swim_Time = 0
    Swim.Swim_Calorie = 0
    Run.Run_Time = 0
    Run.Run_Calorie = 0