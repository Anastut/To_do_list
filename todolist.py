from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()


class Menu:
    def __init__(self):
        self.user_input()

    def user_input(self):
        a = input()
        self.make(a)

    def today_task(self):
        print(f'\nToday {today.day} {today.strftime("%b")}:')
        rows = session.query(Table).filter(Table.deadline == today).all()
        if rows == []:
            print('Nothing to do!')
        else:
            n = 1
            for row in rows:
                print(f'{n}. {row.task}')
                n += 1
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.user_input()

    def week_tasks(self):
        x = 0
        for day in range(7):
            day = today + timedelta(days=x)
            print(f'\n{day.strftime("%A")} {day.day} {day.strftime("%b")}:')
            x += 1
            rows = session.query(Table).filter(Table.deadline == day.date()).all()
            if rows == []:
                print('Nothing to do!')
            else:
                n = 1
                for row in rows:
                    print(f'{n}. {row.task}')
                    n += 1
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.user_input()

    def all_tasks(self):
        print('\nAll tasks:')
        rows = session.query(Table).all()
        task = 1
        for row in rows:
            print(f'{task}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
            task += 1
        return self.user_input()

    def add_task(self, *new_task):
        new_row = Table(task=new_task[0], deadline=datetime.strptime(new_task[1], '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print("The task has been added!\n\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.user_input()

    def missed_tasks(self):
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        if rows == []:
            print('Nothing is missed!')
        else:
            n = 1
            for row in rows:
                print(f'{n}. {row.task}')
                n += 1
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.user_input()

    def delete_task(self, task_to_delete):
        rows = session.query(Table).all()
        task = 1
        print("Chose the number of the task you want to delete:\n")
        for row in rows:
            print(f'{task}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
            task += 1
        specific_row = rows[task_to_delete - 1]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!\n\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.user_input()

    def make(self, command):
        if command == '1':
            return self.today_task()
        if command == '2':
            return self.week_tasks()
        if command == '3':
            return self.all_tasks()
        if command == '4':
            return self.missed_tasks()
        if command == '5':
            new_task = []
            task = input('\nEnter task\n')
            deadline = input('Enter deadline\n')
            new_task.append(task)
            new_task.append(deadline)
            return self.add_task(*new_task)
        if command == '6':
            task_to_delete = int(input())
            return self.delete_task(task_to_delete)
        if command == '0':
            print('\nBye!')


print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")

todo = Menu()
