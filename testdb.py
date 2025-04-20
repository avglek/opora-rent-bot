import json
from sqlalchemy import create_engine
#from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
#from sqlalchemy import  Column, Integer, String

from src.models import Category,Base,Rent,Price
from config import Config,load_config

config: Config = load_config()

engine = create_engine(config.db.get_local_url())

print("Local url:",config.db.get_local_url())

try:
    Base.metadata.create_all(bind=engine)

    with Session(autoflush=False, bind=engine) as db:
        # получение всех объектов
        categories = db.query(Category).all()
        for p in categories:
            print(f"{p.name}")

        rent = db.query(Rent).first()
        print(f"{rent.name} {rent.price.month}")
        print(rent.description)

        cat = db.get(Category,4)
        print("--------")
        print(cat.name)
        rents = cat.rents
        for r in rents:
            print(r.name)

except Exception as e:
    print('Error:',e)