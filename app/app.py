
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash
from datetime import date


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


engine = create_engine(
    "mysql+pymysql://root:rootpassword@mysql_db_container:3306/catgram?charset=utf8mb4")
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    username = Column('username', String(250), nullable=False, unique=True)
    password = Column('password', String(250), nullable=False)

class Cat(Base):
    __tablename__ = 'cats'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    owner_id = Column('owner_id', String(250), nullable=False)
    name = Column('name', String(250), nullable=False)
    color = Column('color', String(250), nullable=False)
    emoji = Column('emoji', String(250), nullable=False)

class CatWeight(Base):
    __tablename__ = 'cat_weights'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    cat_id = Column('cat_id', Integer, nullable=False)
    weight_grams = Column('color', Integer, nullable=False)
    date = Column('date', DateTime, nullable=False)

# Create tables.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db = Session()

# Create sample data if it does not exist yet.
user = db.query(User).filter_by(username="roger-federer").first()
if user is None:
    user = User(username="roger-federer", password=generate_password_hash("rivella-123"))
    db.add(user)
db.commit()

cat1 = db.query(Cat).filter_by(name="Tobi", owner_id=user.id).first()
if cat1 is None:
    cat1 = Cat(name="Tobi", color="black", emoji="😽", owner_id=user.id)
    db.add(cat1)
cat2 = db.query(Cat).filter_by(name="Schnüggi", owner_id=user.id).first()
if cat2 is None:
    cat2 = Cat(name="Schnüggi", color="brown", emoji="😻", owner_id=user.id)
    db.add(cat2)
cat3 = db.query(Cat).filter_by(name="Lollipop", owner_id=user.id).first()
if cat3 is None:
    cat3 = Cat(name="Lollipop", color="white", emoji="😸", owner_id=user.id)
    db.add(cat3)
db.commit()

weight1 = db.query(CatWeight).filter_by(cat_id=cat1.id).first()
if weight1 is None:
    weight1 = CatWeight(cat_id=cat1.id, weight_grams=530, date=date.today())
    db.add(weight1)
db.commit()

weight2 = db.query(CatWeight).filter_by(cat_id=cat2.id).first()
if weight2 is None:
    weight2 = CatWeight(cat_id=cat2.id, weight_grams=348, date=date.today())
    db.add(weight2)
db.commit()

weight3 = db.query(CatWeight).filter_by(cat_id=cat3.id).first()
if weight3 is None:
    weight3 = CatWeight(cat_id=cat3.id, weight_grams=590, date=date.today())
    db.add(weight3)
db.commit()


# It is important that 'import routes' comes last and directly before app.run.
from modules import index, auth, cat_add, cat_weight_add # fmt: skip

if __name__ == '__main__':
    app.run(host='0.0.0.0')
