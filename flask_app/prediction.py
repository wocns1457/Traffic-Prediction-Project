import os 
import pickle
import xgboost
import pandas as pd
from flask_app.traffic_api import *

def pred(input, logs, conn, cur):
   input_list = ['종로구', '용산구', '중구',
               '은평구', '마포구', '도봉구','노원구', '광진구', '중랑구',
               '동대문구', '성북구', '영등포구', '동작구', '관악구', '금천구',
               '강서구', '양천구', '구로구','강남구', '서초구', '송파구','강동구']
   
   if input[0] in input_list:
      try:
         for i in range(len(input)):
            if i != 0:
               input[i] = float(input[i])
         #encoder_FILEPATH = os.path.join(os.getcwd(), 'my_app\\encoder.pkl')
         with open('encoder.pkl','rb') as pickle_file:
            encoder = pickle.load(pickle_file)
            
         #model_FILEPATH = os.path.join(os.getcwd(), 'my_app/xgb_model.model')
         model = xgboost.XGBRegressor() # 모델 초기화
         model.load_model('xgb_model.model')
         columns=['spot_name','pm10', "pm25", "O3", "NO2", "CO", "SO2", "hour"]
         input_df = pd.DataFrame([input], columns=columns)
         
         input_df_encoder = encoder.transform(input_df)   # encoding

         result = model.predict(input_df_encoder)
         result = result.tolist()
         trans_pred(input, result[0], logs, conn, cur)   # 예측값 DB에 저장
         
         return str(result[0])
      
      except ValueError:
         return '옳바른 정보를 입력해 주세요.'
   
   else:
      return '옳바른 정보를 입력해 주세요.'

