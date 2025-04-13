from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.models import Category,Base,Rent,Price
from config import Config,load_config

config: Config = load_config()

engine = create_engine(config.db.get_local_url())

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print('Can`t establish connection to database:',e)

def get_category_kb()->dict[str,str]:
        with Session(autoflush=False, bind=engine) as db:
        # получение всех объектов
            categories = db.query(Category).all()
            result = dict()

            for p in categories:
                result[f"sb-{p.id}"] = p.name

            return result
