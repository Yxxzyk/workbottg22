from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_phone = Column(String)
    user_email = Column(String)
    telegram_id = Column(String)

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    name_cars = Column(String)
    price_cars = Column(String)

class Arenda(Base):
    __tablename__ = 'arenda'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    name_cars = Column(String)
    date_arenda = Column(String)
    price = Column(String)

class Database():
    def __init__(self, db_name):
        self.engine = create_engine('sqlite:///' + db_name)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, user_name, user_phone, user_email, telegram_id):
        new_user = User(user_name=user_name, user_phone=user_phone, user_email=user_email, telegram_id=telegram_id)
        self.session.add(new_user)
        self.session.commit()

    def select_user_id(self, telegram_id):
        return self.session.query(User).filter_by(telegram_id=telegram_id).first()

    def db_select_all(self, table_name):
        if table_name == 'users':
            return self.session.query(User).all()
        elif table_name == 'cars':
            return self.session.query(Car).all()
        elif table_name == 'arenda':
            return self.session.query(Arenda).all()

    def __del__(self):
        self.session.close()