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

    def add_task(self):

        new_task = input("\nEnter task\n")
        dead_line = input("Enter deadline\n")
        dead_line = datetime.strptime(dead_line, "%Y-%m-%d")
        # rows = self.session.query(self.Task).all()
        # new_id = len(rows) + 1
        task = self.Task()
        # task.id = new_id
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
        else:
            for i, row in enumerate(rows):
                print(f"{str(i + 1)}. {row.task}")
        print()
        return

    def week_task(self):

        print()
        today = datetime.today()
        for delta in range(7):
            day_of_week = today + timedelta(days=delta)
            rows = self.session.query(self.Task).filter(self.Task.deadline == day_of_week.date()).all()
            day_week = day_of_week.strftime("%A")
            date_month = str(day_of_week.day)
            month = today.strftime("%b")
            print(f"{day_week} {date_month} {month}:")
            if len(rows) == 0:
                print("Nothing to do!")
            for i, row in enumerate(rows):
                print(f"{str(i + 1)}. {row.task}")
            print()
        return

    def all_task(self):

        print("\nAll tasks:")
        rows = self.session.query(self.Task).order_by(self.Task.deadline).all()
        if len(rows) == 0:
            print("Nothing to do!")
        for i, row in enumerate(rows):
            date = row.deadline
            print(f"{str(i + 1)}. {row.task}. {date.strftime('%d %b')}")
        print()
        return

    def delete_tasks(self):
        print("\nChoose the number of the task you want to delete:")
        rows = self.session.query(self.Task).order_by(self.Task.deadline).all()
        if len(rows) == 0:
            print("Nothing to delete")
        for i, row in enumerate(rows):
            date = row.deadline
            print(f"{str(i + 1)}. {row.task}. {date.strftime('%d %b')}")
        id_r = int(input())
        del_row = rows[id_r-1]
        self.session.delete(del_row)
        self.session.commit()
        print("The task has been deleted!")
        return

    def missed_tasks(self):

        print("\nMissed tasks:")
        rows = self.session.query(self.Task).filter(self.Task.deadline < datetime.today().date()).order_by(self.Task.deadline).all()
        if len(rows) == 0:
            print("Nothing is missed")
        for i, row in enumerate(rows):
            date = row.deadline
            day = str(date.day)
            month = date.strftime("%b")
            print(f"{str(i + 1)}. {row.task}. {day} {month}")
        print()
        return

    def cli(self):

        while True:
            choice = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete "
                           "task\n0) Exit\n")
            if choice == '0':
                print("\nBye!")
                self.session.close()
                return
            elif choice == '1':
                self.today_task()
            elif choice == '2':
                self.week_task()
            elif choice == '3':
                self.all_task()
            elif choice == '4':
                self.missed_tasks()
            elif choice == '5':
                self.add_task()
                print("The task has been added!\n")
            elif choice == '6':
                self.delete_tasks()


if __name__ == '__main__':
    task_list = ToDo_List('todo_list_2.db')
    task_list.cli()
