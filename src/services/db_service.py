from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.models import Category,Base,Rent,Price,RentCallbackFactory,CategoryCallbackFactory,PriceCallbackFactory
from config import Config,load_config

config: Config = load_config()

engine = create_engine(config.db.get_local_url())

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print('Can`t establish connection to database:',e)

def get_category()->dict[str,str]:
        with Session(autoflush=False, bind=engine) as db:
        # получение всех объектов
            categories = db.query(Category).all()
            result = dict()

            for p in categories:
                result[CategoryCallbackFactory(category_id=p.id,name=p.name).pack()] = p.name

            return result

def get_rents_by_id(id:int)->dict[str,str]:
     with Session(autoflush=False,bind=engine) as db:
          # получение списка аренд в группе
          category =  db.get(Category,id)
          rents = category.rents
          result = dict()

          for p in rents:
               result[RentCallbackFactory(rent_id=p.id).pack()] = p.name

          return result

def get_price_by_rent_id(id:int)->dict[str,str]:
    with Session(autoflush=False,bind=engine) as db:
        rent = db.get(Rent,id)

        price = rent.price
        result = dict()

        result[PriceCallbackFactory(price_id=price.id).pack()] = str(price)
