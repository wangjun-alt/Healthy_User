import datetime

def GetUserAge(User_Borntime):
    now_time = datetime.datetime.now()
    year = int(now_time.year)
    month = int(now_time.month)
    day = int(now_time.day)
    yeared = int(User_Borntime[0:4])
    monthed = int(User_Borntime[5:7])
    dayed = int(User_Borntime[8:-1])
    if year < yeared:
        result = 0
    else:
        if month >= monthed and day >= dayed:
            result = year - yeared
        else:
            result = year - yeared
    return result


def GetUserBMI(User_Weight, User_Height):
    BMI = float(User_Weight) / (float(User_Height) * float(User_Height))
    return BMI
