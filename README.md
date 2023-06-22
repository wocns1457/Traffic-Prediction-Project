## 서울시 지역구 교통량 예측 프로젝트
서울시 지역구별 교통량 데이터와 대기환경 데이터를 사용하여 머신러닝 기법을 통해 교통량을 예측하는 Web API 서비스 배포 프로젝트입니다.  

## 1. 데이터 선정 이유 및 문제 정의
자동차에서 배기가스를 통해 발생되는 성분들의 대부분은 오존과 미세먼지등 대기오염에 큰 영향을 미치는 요소들 중 하나입니다.
또한 교통량이 증가했다는 것은 배기가스를 통해 발생되는 성분들이 더 많아졌다는 것으로 대기오염의 문제로 이어지게 됩니다.
이러한 관계를 이용하여 서울시 지역구별 교통량과 대기환경 데이터를 사용해 교통량을 예측하는 **회귀 문제**로 정의할 수 있습니다.  
또한 사용자가 이 서비스를 통해 필요에 따라 자신이 위치하고 있는 지역에 교통량을 예측할 수 있게 됩니다.

[서울시 열린 데이터 광장](https://data.seoul.go.kr/)에서 제공하는 Open API를 이용하여 데이터를 수집하였습니다. 

교통량 데이터 : https://data.seoul.go.kr/dataList/OA-13316/A/1/datasetView.do  
대가환경 데이터 : https://data.seoul.go.kr/dataList/OA-2221/S/1/datasetView.do

## 2. 데이터 구성
- 2021년 1월~3월 서울시 21개의 지역구별 교통량, 대기환경 관측 데이터
- 총 25개의 지역구에서 서대문구, 강북구, 성동구, 송파구는 누락된 값이 많아 제거.
- Total : 10250개
- 교통량 관측 데이터  
  - Spot num : 해당 지역구에 있는 관측소 ID 
  - Vol : 교통량

<img src = "https://github.com/wocns1457/Traffic-Prediction-Project/blob/main/images/img1.JPG" width="70%" height="70%">

- 대기환경 관측 데이터  
  - Pm10 : 미세먼지 농도
  - Pm25 : 초미세먼지 농도
  - O3 : 오존
  - NO2 : 이산화질소농도
  - CO : 일산화탄소농도
  - SO2 : 아황산가스농도

<img src = "https://github.com/wocns1457/Traffic-Prediction-Project/blob/main/images/img2.JPG" width="70%" height="70%">  

- 데이터 전처리, 시각화는 [model.ipynb](https://github.com/wocns1457/Traffic-Prediction-Project/blob/main/model.ipynb)에 설명되어 있습니다.

## 3.데이터 파이프라인  
<p align="center">
<img src = "https://github.com/wocns1457/Traffic-Prediction-Project/blob/main/images/img3.JPG" width="70%" height="70%">
<p/>  

## 4. 모델 결과
- Training : 8277개, Val : 1461개, Test : 513개
- Model : XGBoost Regressor
- Baseline Model
  -  MAE: 193.445
- XGBoost
  - MAE: 49.903
  - MSE: 6178.445
  - R2: 0.896

## 5. 웹 페이지, 대시보드
<p align="center">
  <img src = "https://github.com/wocns1457/Traffic-Prediction-Project/blob/main/images/gif2.gif" width="85%" height="85%">
<img src = "https://github.com/wocns1457/Traffic-Prediction-Project/blob/main/images/gif1.gif" width="85%" height="85%">
<p/>
