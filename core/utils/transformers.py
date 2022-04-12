import datetime

postTypeIntToStr = {
    1: '자유',
    2: '정보',
}


def getLevelRequiredProtein(level):
    if level == 1:
        return 100
    elif level == 2:
        return 1000
    elif level == 3:
        return 10000
    elif level == 4:
        return 50000
    elif level == 5:
        return 100000
    elif level == 6:
        return 200000
    else:
        return 0


def zeroAdder(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


def timeCalculator(date_time):
    delta = (datetime.datetime.now() - date_time.replace(tzinfo=None)).seconds
    if datetime.date.today() != date_time.date():
        return zeroAdder(date_time.month) + "/" + zeroAdder(date_time.day)
    elif delta // 3600 > 0:
        return zeroAdder(date_time.hour) + ":" + zeroAdder(date_time.minute)
    else:
        return str(delta // 60) + "분 전"
        

activityLevelIntToStr = {
    0: '말랑말랑 인간',
    1: '헬스세포',
    2: '헬린이',
    3: '말하는 닭가슴살',
    4: '근성장 교과서',
    5: '걸어다니는 헬스장',
    6: '근손실 방지 위원회', 
}