import os
import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import date, timedelta

class MONGODB_SETUP:
    def __init__(self, start_y, start_m, start_d, end_y, end_m, end_d):

        self.KEY = 'Insert api key'
        self.TYPE = 'json'
        self.HOURS = ['00', '04', '08', '12', '16', '20']

        self.TEXT_FILENAME = '교통량지점정보.txt'
        self.TEXT_FILEPATH = os.path.join(os.getcwd(), self.TEXT_FILENAME)

        self.HOST = 'Insert Host'
        self.USER = 'Insert user'
        self.PASSWORD = 'Insert password'
        self.DATABASE_NAME = 'Insert DB name'
        self.COLLECTION_VOL = 'VOL_LIST'
        self.COLLECTION_WEATHER = 'WEATHER_LIST'

        self.MONGO_URI = 'Insert URI'
        self.API_KEY = 'Insert API KEY'
        
        self.start_date = date(start_y, start_m, start_d) 
        self.end_date = date(end_y, end_m, end_d) 
        
        client = MongoClient(self.MONGO_URI)
        db = client[self.DATABASE_NAME]
        self.collection_vol = db[self.COLLECTION_VOL]
        self.collection_weather = db[self.COLLECTION_WEATHER]


    def daterange(self):  # ex daterange(date(2021, 3, 1))
        for n in range(int((self.end_date - self.start_date).days)): 
            yield self.start_date + timedelta(n) 


    def get_spot(self):
        f = open(self.TEXT_FILEPATH, 'r', encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            spot = [line.strip().split('/')[2] for line in lines]
        f.close()
        return spot    
    
    
    def set_wheather(self):
        for single_date in self.daterange(): 
            day = single_date.strftime("%Y%m%d")
            for hour in self.HOURS:
                API_URL = f'http://openAPI.seoul.go.kr:8088/{self.KEY}/{self.TYPE}/TimeAverageCityAir/1/25/{day}{hour}00'
                response = requests.get(API_URL)   
                time.sleep(0.3)
            
                if response.status_code == 200:
                    pass
                else:
                    print("response status_code is NOT 200")
                    print(f"sensor api end page: {day}")
                    break  
                weather = response.json()
                self.collection_weather.insert_many(weather['TimeAverageCityAir']['row'])
                
                
    def set_vol(self):
        spots = self.get_spot()
        for single_date in self.daterange(): 
            day = single_date.strftime("%Y%m%d")
            for spot in spots:
                result=[]
                for hour in self.HOURS:
                    XML_URL = f"http://openapi.seoul.go.kr:8088/{self.KEY}/xml/VolInfo/1/5/{spot}/{day}/{hour}/"
                    page = requests.get(XML_URL)
                    time.sleep(0.3)
                        
                    if page.status_code == 200:
                        pass
                    else:
                        print("response status_code is NOT 200")
                        print(f"sensor api end page: {day}")
                        break  
                    
                    soup = BeautifulSoup(page.content, 'html.parser')
                    infoms = soup.find_all(['row'])
                    
                    for infom in infoms:
                        spot_num = infom.find('spot_num').text
                        ymd = infom.find('ymd').text
                        hh = infom.find('hh').text
                        vol = infom.find('vol').text
                        result.append({'ymd':ymd+hh+'00', 'vol':vol})
                        break
            
                dic = {'date':day, 'spot_num':spot_num, "result":result}            
                self.COLLECTION_VOL.insert_one(dic)


    def get_weather(self):
        docs = self.collection_weather.find({})
        return docs
    
    
    def get_vol(self):
        docs = self.collection_vol.find({})
        return docs

#mongo = MONGODB_SETUP(2021, 3, 1, 2021, 4, 1)




