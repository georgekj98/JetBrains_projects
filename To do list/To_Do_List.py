from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


class ToDo_List():
    Base = declarative_base()

    class Task(Base):

        __tablename__ = "task"
        id = Column('id', Integer, primary_key=True)
        task = Column('task', String)
        deadline = Column('deadline', Date, default=datetime.today())

    def __init__(self, db_name):

        engine = create_engine(f'sqlite:///{db_name}?check_same_thread=False')
        self.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def print_tasks(self):

        print("\nToday:")
        rows = self.session.query(self.Task).all()
        if len(rows) == 0:
            print("Nothing to do!")
        for i, row in enumerate(rows):
            print(f"{str(i+1)}. {row.task}")
        print()
        return

    def add_task(self):

        new_task = input("\nEnter task\n")
        dead_line = input("Enter deadline\n")
        dead_line = datetime.strptime(dead_line, "%Y-%m-%d")
        rows = self.session.query(self.Task).all()
        new_id = len(rows) + 1
        task = self.Task()
        task.id = new_id
        task.task = new_task
        task.deadline = dead_line
        self.session.add(task)
        self.session.commit()
        return

    def today_task(self):

        today = datetime.today()
        rows = self.session.query(self.Task).filter(self.Task.deadline == today.date()).all()
        day = str(today.day)
        month = today.strftime("%b")
        print(f"\nToday {day} {month}:")
        if len(rows) == 0:
            print("Nothing to do!")
        for i, row in enumerate(rows):
            print(f"{str(i + 1)}. {row.task}")
        print()
        return

    def week_task(self):
        pass

    def all_task(self):

        print("\nAll tasks:")
        rows = self.session.query(self.Task).all()
        if len(rows) == 0:
            print("Nothing to do!")
        for i, row in enumerate(rows):
            date = row.deadline
            day = str(date.day)
            month = date.strftime("%b")
            print(f"{str(i + 1)}. {row.task}. {day} {month}")
        print()
        return

    def cli(self):

        while True:
            choice = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit\n")
            if choice == '0':
                print("\nBye!")
                return
            elif choice == '1':
                self.today_task()
            elif choice == '4':
                self.add_task()
                print("The task has been added!\n")
            elif choice == '3':
                self.all_task()


if __name__ == '__main__':
   task_list = ToDo_List('todo_list.db')
   task_list.cli()
   ''' engine = create_engine('sqlite:///todo_list.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    # Task.__table__.create(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    cli()
    #Base.metadata.drop_all(bind=engine)
    session.close()'''


''' def list_out():
        print("Today:")
        print("1) Do yoga")
        print("2) Make breakfast")
        print("3) Learn basics of SQL")
        print("4) Learn what is ORM")


list_out()'''

