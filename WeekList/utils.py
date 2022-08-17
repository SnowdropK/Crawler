import time  # 引入time模块

# timestamp = time.time()
# 查询的时间范围
# ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S,%f'
# theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
# currentTime = datetime.now()

# 获取时间戳
def getTimeStamp(currentDateTime):
    # 规范时间格式
    # dd = datetime.datetime.strptime(currentDateTime, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    timeStamp = int(time.mktime(time.strptime(currentDateTime, '%Y-%m-%d %H:%M:%S')))
    return timeStamp


