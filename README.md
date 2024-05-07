# Crypto_Currency


## 1. 프로젝트 소개
-----------------
트위터 api를 통해 bitcoin, ethereum 이 포함된 트윗을 실시간으로 kafka로 데이터를 불러온 뒤, 효율적인 감성 분석을 위해 spark에서 데이터 전처리 과정을 거친 뒤, nlkt 라이브러리를 통해 감성 분석을 진행합니다. 감성 분석의 결과는 mongo db에 저장되고, 이를 바탕으로 암호화폐의 가격과 트윗 감성 분석의 결과의 상관 관계를 분석하였습니다.
이더리움과 비트고인의 가격은 binance의 ccxt 라이브러리를 통해 받아와, highchart 라이브러리를 통해 상관관계를 시각화하였습니다.

## 2. 프로젝트 구조
![프로젝트 구조](https://user-images.githubusercontent.com/47740690/127730925-b4fd7664-9e6b-4fb9-9a33-b4b2dcd0221b.PNG)

## 3. 결과

#### 실시간 비트코인/이더리움 가격 차트

![차트](https://user-images.githubusercontent.com/47740690/127730955-9e36b570-4857-4990-86fa-90a54930260a.PNG)

#### 암호화폐 가격과 트윗 감성 분석 간의 상관 관계
<img src="https://user-images.githubusercontent.com/47740690/127730871-e4898b01-be1a-45a5-a13b-d567d885c65f.PNG" width="700" height="400" >

위와 같은 결과로 암호화폐의 가격과 트윗의 감성 분석 간의 유의미한 결과를 얻어내었습니다. 하지만, 특정 사건에 의해 트윗이 갑자기 많이 몰리는 경우도 있어 추후에 이 부분에 관한 보완이 필요해 보입니다.
