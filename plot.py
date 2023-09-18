from pymongo import MongoClient
import pymongo
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
# 从环境变量中获取Secrets变量的值
db_connection_string = os.environ.get('DB_CONNECTION_STRING')

client = MongoClient(db_connection_string)  # 根据实际情况更改连接字符串
db = client['radiation']
collection = db['radiation']

def dose_plot():
    data = list(collection.find().sort([("_id", pymongo.DESCENDING)]).limit(28))
    new_data = []
    for point in data:
        # 从ObjectId中提取时间戳
        time_tag = point['_id'].generation_time.timestamp()
        date_time = datetime.fromtimestamp(time_tag)
        clean_data = {'time': date_time, 'SensorID': point['sensor_id'], 'CPM': point['CPM'], 'Dose': point['Dose']}
        new_data.append(clean_data)

    
    times = [entry['time'] for entry in new_data]
    dose_rate = [float(entry['Dose']) for entry in new_data]

    # 创建图表
    plt.figure(figsize=(16, 10))
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(left=0.09, right=0.98, top=0.93, bottom=0.19)
    # 手动设置纵坐标刻度
    plt.ylim(0, 2)
    plt.plot(times, dose_rate, marker='o', linestyle='-', color='black')
    plt.title('Latest 7-day monitoring value', fontsize=30)
    plt.ylabel('Equivalent dose rate (μSv/h)', fontsize=30)
    # 将纵坐标范围从0开始
    # 格式化横坐标刻度为日期和时间
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(times, rotation=90)  # 旋转横坐标标签以避免重叠
    plt.grid(True)

    # 添加y轴参考线
    plt.axhline(y=0.13, color='blue', linestyle='--', label='Reference Line: 0.13 μSv/h')
    # 添加y轴参考线
    plt.axhline(y=0.5, color='red', linestyle='--', label='Reference Line: 0.5 μSv/h')

    # 添加图示文本
    plt.text(0.75, 0.83, 'Background level:0.13 μSv/h', fontsize=17, color='blue', transform=plt.gca().transAxes)
    plt.text(0.75, 0.79, 'Hazard level:0.5 μSv/h', fontsize=17, color='red', transform=plt.gca().transAxes)

    plt.savefig('public/assets/dose_vs_time.svg', format='svg')

dose_plot()
