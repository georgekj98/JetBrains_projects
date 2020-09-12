from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Task(Base):

    __tablename__ = "task"
    id = Column('id', Integer, primary_key=True)
    task = Column('task', String)
    deadline = Column('deadline', Date, default=datetime.today())


def main():

    engine = create_engine('sqlite:////todo.db?check_same_thread=False', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()

''' def list_out():
        print("Today:")
        print("1) Do yoga")
        print("2) Make breakfast")
        print("3) Learn basics of SQL")
        print("4) Learn what is ORM")


list_out()'''

