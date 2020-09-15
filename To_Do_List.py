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


def print_tasks():

    print("\nToday:")
    rows = session.query(Task).all()
    if len(rows) == 0:
        print("Nothing to do!")
    for i, row in enumerate(rows):
        print(f"{str(i+1)}. {row.task}")
    print()
    return


def add_task(new_task):
    rows = session.query(Task).all()
    new_id = len(rows) + 1
    task = Task()
    task.id = new_id
    task.task = new_task
    session.add(task)
    session.commit()
    return


def cli():

    choice = 123
    while choice:
        choice = input("1) Today's tasks\n2) Add task\n0) Exit\n")
        if choice == '0':
            print("\nBye!")
            return
        elif choice == '1':
            print_tasks()
        elif choice == '2':
            new_task = input("\nEnter task\n")
            add_task(new_task)
            print("The task has been added!\n")


if __name__ == '__main__':
    engine = create_engine('sqlite:////todo_list.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    # Task.__table__.create(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    cli()
    #Base.metadata.drop_all(bind=engine)
    session.close()


''' def list_out():
        print("Today:")
        print("1) Do yoga")
        print("2) Make breakfast")
        print("3) Learn basics of SQL")
        print("4) Learn what is ORM")


list_out()'''

