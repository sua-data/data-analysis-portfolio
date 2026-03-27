# Employment News Classifier

## 프로젝트 소개

고용 관련 뉴스 기사를 자동으로 분류하는 머신러닝 기반 웹 서비스입니다.
엑셀 데이터(라벨링된 기사 제목)를 활용하여 모델을 학습하고,
입력된 기사 제목이 "고용기사"인지 "비고용기사"인지 예측합니다.

---

## 프로젝트 목적

* 텍스트 데이터를 활용한 머신러닝 분류 모델 구현
* FastAPI를 활용한 백엔드 API 구축
* 데이터 전처리 → 학습 → 예측 → 시각화까지 전체 파이프라인 경험

---

## 사용 기술

### Backend

* FastAPI
* Python

### Database

* MySQL (SQLAlchemy, PyMySQL)

### Data Analysis / ML

* Pandas
* Scikit-learn
* TF-IDF Vectorizer
* Logistic Regression

### Visualization

* Matplotlib

---

## 프로젝트 구조

```
03-employment-news-classifier/
│
├── main.py           # FastAPI 실행 및 라우팅
├── db.py             # DB 연결
├── logger.py         # 로그 관리
├── news_model.py     # 데이터 처리 / 모델 학습 / 예측
├── requirements.txt
│
├── data/             # 원본 엑셀 데이터
├── model/            # 학습된 모델 저장
├── fig/              # 그래프 이미지
└── view/             # HTML 페이지
```

---

## 주요 기능

### 1. 데이터 전처리 및 저장

* 여러 엑셀 파일을 읽어 하나의 데이터셋으로 통합
* 라벨러 결과를 기반으로 고용기사 여부 생성
* 중복 제거 및 결측치 처리
* MySQL DB에 저장

---

### 2. 머신러닝 모델 학습

* TF-IDF를 이용한 텍스트 벡터화
* Logistic Regression을 이용한 분류 모델 학습
* 불균형 데이터 처리를 위한 class_weight 적용
* 모델을 파일로 저장 (joblib)

---

### 3. 뉴스 기사 분류 (예측)

* 입력된 기사 제목을 기반으로 확률 계산
* threshold 기준으로 고용기사 / 비고용기사 분류

---

### 4. 데이터 시각화

* 실제 데이터 vs 모델 예측 결과 비교
* Matplotlib을 이용한 그래프 생성

---

## 실행 방법

### 1. 가상환경 생성 및 활성화

```
python -m venv .venv
.venv\Scripts\activate
```

### 2. 라이브러리 설치

```
pip install -r requirements.txt
```

### 3. DB 설정

db.py 파일에서 본인의 DB 정보로 수정

```
user = "web_user"
password = "your_password"
host = "localhost:3306"
db = "mydb"
```

### 4. 서버 실행

```
uvicorn main:app --reload
```

### 5. 접속

```
http://127.0.0.1:8000
```

---

## API 엔드포인트

| 기능     | URL        | 설명         |
| ------ | ---------- | ---------- |
| 메인 페이지 | /          | index.html |
| 데이터 저장 | /insert    | 엑셀 → DB    |
| 모델 학습  | /learn     | 모델 학습      |
| 예측     | /predict   | 기사 분류      |
| 그래프    | /showGraph | 시각화        |

---

## 느낀 점 / 개선 방향

* 텍스트 데이터 전처리의 중요성을 체감
* 불균형 데이터 처리의 필요성 이해
* 향후:

  * 더 다양한 모델 비교 (SVM, XGBoost 등)
  * 데이터 확장 및 성능 개선
  * 프론트엔드 UI 개선

---

## 참고

본 프로젝트는 학습 및 포트폴리오 용도로 제작되었습니다.
