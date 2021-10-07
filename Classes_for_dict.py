from datetime import datetime, date, timedelta
import json
import os
import csv
from abc import ABC, abstractmethod


class Files(ABC):
    """Междумордие(но получилась абстракция) стратегии"""
    extensions = ['.json', '.csv']

    @classmethod
    @abstractmethod
    def userslist(cls) -> list:
        ...
        # !!!! ПОКА НЕ СТИРАТЬ

        # filelist = []
        # for file in os.listdir('./users/'):
        #     for extension in cls.extensions:
        #         if file[-len(extension):] == extension:
        #             filelist.append(file.rstrip(extension))
        # return filelist

    @classmethod
    def deluser(cls, name: str):
        for extension in cls.extensions:
            try:
                os.remove('./users/' + name + extension)
            except FileNotFoundError:
                pass

    @staticmethod
    @abstractmethod
    def adduser(name: str):
        ...

    @staticmethod
    @abstractmethod
    def opentasks(name: str) -> list:
        ...

    @staticmethod
    @abstractmethod
    def safetasks(name: str, data: list) -> None:
        ...


class JsonFile(Files):

    @classmethod
    def userslist(cls) -> list:
        filelist = []
        for file in os.listdir('./users/'):
            if file[-len('.json'):] == '.json':
                filelist.append(file.rstrip('.json'))
        return filelist

    @staticmethod
    def adduser(name: str):
        newuser = Task().__dict__
        newuser.pop('counter')
        try:
            with open('./users/' + name + '.json', 'w') as f:
                json.dump([newuser], f)
        except FileNotFoundError:
            os.mkdir('users')
            with open('./users/' + name + '.json', 'w') as f:
                json.dump([newuser], f)

    @staticmethod
    def opentasks(name: str) -> list:
        with open('./users/' + name + '.json', 'r') as file_json:
            data = json.load(file_json)
        return data

    @staticmethod
    def safetasks(name: str, data: list) -> None:
        with open('./users/' + name + '.json', 'w') as file_json:
            json.dump(data, file_json)

    def __repr__(self):
        return 'JSON'


class CsvFile(Files):

    @classmethod
    def userslist(cls) -> list:
        filelist = []
        for file in os.listdir('./users/'):
            if file[-len('.csv'):] == '.csv':
                filelist.append(file.rstrip('.csv'))
        return filelist

    @staticmethod
    def adduser(name: str):
        newuser = Task().__dict__
        newuser.pop('counter')
        try:
            with open('./users/' + name + '.csv', 'w') as f:
                pass
        except FileNotFoundError:
            os.mkdir('users')
        with open('./users/' + name + '.csv', 'w') as f:
            names = list(newuser.keys())
            writer = csv.DictWriter(f, fieldnames=names)
            writer.writeheader()
            writer.writerow(newuser)

    @staticmethod
    def opentasks(name: str) -> list:
        csv_list = []
        with open('./users/' + name + '.csv', 'r') as f:
            file_reader = csv.DictReader(f)
            for row in file_reader:
                csv_list.append(row)
        return csv_list

    @staticmethod
    def safetasks(name: str, data: list) -> None:
        with open('./users/' + name + '.csv', 'w') as f:
            names = list(data[0].keys())
            writer = csv.DictWriter(f, fieldnames=names)
            writer.writeheader()
            for line in data:
                writer.writerow(line)

    def __repr__(self):
        return 'CSV'


class Task:
    counter = 0

    def __init__(self, name: str = 'Test_task', description: str = 'Test_description',
                 deadline=date.today().strftime('%Y-%m-%d'),
                 created=date.today().strftime('%Y-%m-%d'), done=False):
        self.name = name
        self.description = description
        self.created = created
        self.deadline = deadline
        self.done = done
        self.counter = Task.counter
        Task.counter += 1

    @classmethod
    def instances(cls):
        return cls.counter + 1

    @staticmethod
    def att2create():
        return [['name', 'Name'], ['description', 'Description'], ['deadline', 'deadline - "YYYY-MM-DD']]

    @staticmethod
    def att():
        return ['name', 'description', 'created', 'deadline']

    def attributes(self) -> list:
        att = list(self.__dict__.keys())
        att.remove('counter')
        att.remove('done')
        return att

    def edit(self, name=None, description=None,
             deadline=None,
             created=None):
        if name != None:
            self.name = name
        if description != None:
            self.description = description
        if deadline != None:
            self.deadline = deadline
        if created != None:
            self.created = created


class Tasks:

    def __init__(self, user=None, strategy: Files = JsonFile, readonly=False):
        self.task_list = []
        self.strategy = strategy
        self.readonly = readonly
        if user == None:
            self.__user = 'Test_user'
            self.task_list.append(Task())  # пустая задача
        else:
            self.__user = user
            self.addlisttasks(strategy.opentasks(self.__user))

    # вроде не используется
    # !!! уже используется!!!
    @property
    def user(self):
        return self.__user

    # !!!!!!!!!!!!! пока не удалять!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # @user.setter
    # def user(self, name):
    #     os.remove('./users/' + self.__user + '.json')
    #     self.__user = name
    #     self.safetasks()

    def changeuser(self, name):
        self.task_list = []
        self.__user = name
        self.strategy.opentasks(self.__user)

    def addtask(self, *args, **kwargs) -> None:
        if args == () and kwargs == {}:
            pass
        else:
            self.task_list.append(Task(*args, **kwargs))

    def addlisttasks(self, tasks: list):
        for el in tasks:
            self.task_list.append(Task(**el))

    def deltasks(self, *args: int) -> None:
        ''' args this is Task counters
        '''
        for num, el in enumerate(self.task_list):
            if el.counter in args:
                self.task_list.pop(num)

    def edittask(self, counter: int, **kwargs) -> None:
        for i in self.task_list:
            if i.counter == counter:
                i.edit(**kwargs)

    def showtasks(self, lbl=True) -> list:
        tasklist = []
        if lbl == True:
            for task in self.task_list:
                print(task.__dict__)
        else:
            for task in self.task_list:
                tasklist.append(task.__dict__)
            return tasklist

    def shownames(self, *args) -> list:
        ''' *args - counters
        return list of names
        '''
        nameslist = []
        for task in self.task_list:
            if task.counter in args:
                nameslist.append(task.name)
        return nameslist

    def tasks2save(self) -> list:
        tasklist = []
        for task in self.task_list:
            tmpdict = {}
            listtemp = list(task.__dict__.keys())
            listtemp.remove('counter')
            for task_2 in listtemp:
                tmpdict[task_2] = task.__dict__[task_2]
            tasklist.append(tmpdict)
        return tasklist

    def sorted(self, attribute: str = 'name') -> list:
        tasklist = []
        [tasklist.append(x.__dict__) for x in self.task_list]
        sorted_second = sorted(tasklist, key=lambda x: x['name'])  # second sort (by 'name')
        return sorted(sorted_second, key=lambda x: x[attribute])

    def taskdone(self, *args: int) -> None:
        for el in self.task_list:
            if el.counter in args:
                el.done = True

    def filter(self, text: str, key: str = '*') -> list:
        '''Выводит отсортированный список
        use key - '*' for search in all keys except "counter" and "done" '''
        if key != '*':
            return list(map(lambda x: x.__dict__,
                            list(filter(lambda x: text.lower() in x.__dict__[key].lower(), self.task_list))))
        else:
            tasks = []
            for i in Task.att():
                tasks.append(set(filter(lambda x: text.lower() in x.__dict__[i].lower(), self.task_list)))
            return list(map(lambda x: x.__dict__, list(tasks[0].union(*list(tasks[x] for x in range(1, len(tasks)))))))

    def test(self):
        print(self.task_list)
