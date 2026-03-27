from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.staticfiles import StaticFiles

from logger import Logger
from news_model import insert_data, train_model, predict_category, make_graph

app = FastAPI()
logger = Logger().get_logger(__name__)

# 정적 폴더 연결
app.mount("/view", StaticFiles(directory="view"))
app.mount("/fig", StaticFiles(directory="fig"))


# 메인 페이지
@app.get("/")
def main():
    return RedirectResponse(url="/view/index.html")


# 예측 요청용 모델
class NewsRequest(BaseModel):
    content: str


# 엑셀 데이터를 읽어서 DB에 저장
@app.get("/insert")
def insert():
    try:
        result = insert_data()
        logger.info(result["msg"])
        return RedirectResponse(url="/")
    except Exception as e:
        logger.error(f"insert 오류: {e}")
        return {"msg": "데이터 저장 실패", "error": str(e)}


# 학습
@app.get("/learn")
def learn():
    try:
        result = train_model()
        logger.info("학습 완료")
        return result
    except Exception as e:
        logger.error(f"learn 오류: {e}")
        return {"msg": "학습 실패", "error": str(e)}


# 예측
@app.post("/predict")
def predict(data: NewsRequest):
    try:
        result = predict_category(data.content)
        logger.info(f"예측 결과: {result}")
        return {"category": result}
    except Exception as e:
        logger.error(f"predict 오류: {e}")
        return {"msg": "예측 실패", "error": str(e)}


# 그래프 보여주기
@app.get("/showGraph")
def show_graph():
    try:
        content = make_graph()
        return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"showGraph 오류: {e}")
        return HTMLResponse(content=f"<h3>그래프 생성 실패: {e}</h3>")


# 그래프 페이지로 이동
@app.get("/showGraphPage")
def show_graph_page():
    return RedirectResponse(url="/view/showGraph.html")