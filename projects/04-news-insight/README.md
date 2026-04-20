# 📊 News Insight (경제 뉴스 분석 서비스)

## 1. 프로젝트 개요
경제 뉴스 데이터를 기반으로  
이슈 트렌드 분석, 감성 분석, 키워드 기반 인사이트를 제공하는 서비스입니다.

단순 기사 나열이 아닌  
데이터 분석을 통해 “현재 어떤 이슈가 중요한지”를 한눈에 파악할 수 있도록 합니다.

---

## 2. 주요 기능

- 📰 뉴스 기사 수집
- 🔍 키워드 추출 (TF-IDF + Nori)
- 📊 감성 분석 (긍정/부정/중립)
- 🏆 이슈 키워드 선정
- 📡 API 제공 (FastAPI)
- 🛠 관리자 로그 모니터링

---

## 3. 시스템 흐름


크롤링 → 전처리 → 분석 → 저장 → API → Frontend


---

## 4. 기술 스택

### Backend
- Python, FastAPI

### Data Processing
- Pandas, BeautifulSoup, Selenium

### Analysis
- TF-IDF, Scikit-learn
- Elasticsearch, Nori

### Database
- MySQL / MariaDB

### Infra
- APScheduler

---

## 5. 문서

- 👉 [아키텍처](./docs/architecture.md)
- 👉 [데이터 흐름](./docs/data-flow.md)
- 👉 [트러블슈팅](./docs/troubleshooting.md)

---

## 6. 개발 로그

👉 [Dev Log 보러가기](../../docs/devlog)