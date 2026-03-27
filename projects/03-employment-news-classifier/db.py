from sqlalchemy import create_engine

id="web_user"
pw="your_password"
host="localhost:3306"
db="mydb"
url=f"mysql+pymysql://{id}:{pw}@{host}/{db}"

engine = create_engine(
    url,
    echo=True,
    pool_size=1
)

def get_engine():
    return engine
