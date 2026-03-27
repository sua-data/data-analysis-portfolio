import glob
import os

import matplotlib.pyplot as plt
import pandas as pd
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from db import get_engine
from logger import Logger

logger = Logger().get_logger(__name__)

MODEL_DIR = "model"
FIG_DIR = "fig"
MODEL_PATH = os.path.join(MODEL_DIR, "news.joblib")


def ensure_dirs():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


def insert_data():
    ensure_dirs()

    # 1. 엑셀 파일 전체 가져오기
    files = glob.glob("data/*.xlsx")
    logger.info(f"파일 개수: {len(files)}")

    if not files:
        raise FileNotFoundError("data 폴더에 xlsx 파일이 없습니다.")

    df_list = []

    # 2. 각 엑셀 파일 읽기
    for file in files:
        logger.info(f"읽는 중: {file}")
        df = pd.read_excel(file)
        df_list.append(df)

    # 3. 여러 개의 DataFrame 합치기
    total_df = pd.concat(df_list, ignore_index=True)

    logger.info(f"원본 데이터 크기: {total_df.shape}")
    logger.info(f"컬럼 목록: {list(total_df.columns)}")

    # 4. 라벨러 컬럼 지정
    label_cols = ["라벨러1", "라벨러2", "라벨러3", "라벨러4", "라벨러5", "라벨러6"]

    # 5. 필요한 컬럼만 사용
    total_df = total_df[["제목"] + label_cols]

    # 6. 결측치 제거
    logger.info(total_df.isna().sum())
    total_df.dropna(subset=label_cols, inplace=True)

    # 7. O 개수 세기
    total_df["o_count"] = total_df[label_cols].apply(
        lambda row: sum(row == "O"), axis=1
    )

    # 8. target 만들기
    total_df["target"] = total_df["o_count"].apply(
        lambda x: 1 if x >= 3 else 0
    )

    # 9. 필요한 컬럼만 다시 정리
    total_df = total_df[["제목", "target"]]

    # 10. 컬럼명 변경
    total_df.columns = ["content", "target"]

    # 11. 문자열 공백 제거
    total_df["content"] = total_df["content"].astype(str).str.strip()

    # 12. 빈 문자열 제거
    total_df = total_df[total_df["content"] != ""]

    # 13. 중복 제거
    logger.info(f"중복 개수: {total_df.duplicated().sum()}")
    total_df.drop_duplicates(subset=["content"], inplace=True)

    logger.info(f"전처리 후 데이터 크기: {total_df.shape}")

    # 14. DB 저장
    total_df.to_sql(
        name="employment_news",
        con=get_engine(),
        index=False,
        if_exists="replace"
    )

    logger.info("DB 저장 완료")
    return {"msg": "DB 저장 완료"}


def load_training_data():
    sql = "select content, target from employment_news"
    df = pd.read_sql_query(sql, con=get_engine())

    df.dropna(subset=["content", "target"], inplace=True)
    df["content"] = df["content"].astype(str).str.strip()
    df = df[df["content"] != ""]

    return df


def train_model():
    ensure_dirs()

    # 1. DB에서 학습 데이터 가져오기
    df = load_training_data()

    # 2. 입력(x), 정답(y) 구분
    x = df["content"].astype(str).to_numpy()
    y = df["target"].astype(int).to_numpy()

    # 3. 학습 / 테스트 데이터 분리
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.3,
        random_state=33,
        stratify=y
    )

    # 4. 파이프라인 구성
    model = Pipeline([
        (
            "vect",
            TfidfVectorizer(
                max_df=0.95,
                min_df=2,
                ngram_range=(1, 2)
            )
        ),
        (
            "model",
            LogisticRegression(
                class_weight={0: 1, 1: 7},
                max_iter=1000
            )
        )
    ])

    # 5. 학습
    model.fit(x_train, y_train)

    # 6. 정확도 평가
    score = model.score(x_test, y_test)
    logger.info(f"score = {score}")

    # 7. 상세 성능 평가
    pred = model.predict(x_test)
    report = classification_report(y_test, pred)

    logger.info("\n" + report)
    print(report)

    # 8. 모델 저장
    dump(model, MODEL_PATH)

    return {
        "msg": "학습 완료",
        "score": score,
        "report": report
    }


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("저장된 모델이 없습니다. 먼저 /learn 을 실행하세요.")
    return load(MODEL_PATH)


def predict_category(content: str):
    text = content.strip()
    model = load_model()

    # 예측 확률
    proba = model.predict_proba([text])[0]
    p = proba[1]

    # threshold 기준 분류
    category = "고용기사" if p >= 0.3 else "비고용기사"
    return category


def make_graph():
    # 1. DB에서 데이터 가져오기
    df = load_training_data()

    # 2. 입력 데이터 준비
    x = df["content"].to_numpy()

    # 3. 저장된 모델 불러오기
    model = load_model()

    # 4. 전체 데이터 예측
    pred = model.predict(x)

    # 5. 실제 vs 예측 개수 비교
    label_counts = df["target"].value_counts().sort_index()
    pred_counts = pd.Series(pred).value_counts().sort_index()

    # 6. 한글 폰트 설정
    set_font()

    # 7. 그래프 생성
    graph = plt.figure(figsize=(10, 4))
    plt.style.use("ggplot")

    # 실제 데이터 분포
    plt.subplot(1, 2, 1)
    bars1 = plt.bar(["비고용기사", "고용기사"], label_counts)
    plt.title("실제 데이터 분포", fontsize=12)
    plt.xlabel("기사 종류")
    plt.ylabel("개수")

    for bar in bars1:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    # 모델 예측 분포
    plt.subplot(1, 2, 2)
    bars2 = plt.bar(["비고용기사", "고용기사"], pred_counts)
    plt.title("모델 예측 분포", fontsize=12)
    plt.xlabel("예측 결과")
    plt.ylabel("개수")

    for bar in bars2:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()

    # 8. 이미지 저장
    path = "fig/show_graph.png"
    graph.savefig(path, transparent=True)
    plt.close()

    # 9. HTML 반환
    content = f"<img src='/{path}?v=1'/>"
    return content


def set_font():
    import matplotlib.font_manager as fm

    font_path = "C:/Windows/Fonts/malgun.ttf"
    font_props = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_props.get_name()
    plt.rcParams["axes.unicode_minus"] = False


