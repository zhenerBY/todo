from Classes_for_dict import Task, Tasks, JsonFile, CsvFile, Files
import click


def set_and_val(text: str, conditions: list = None, texterr: str = None, check=False, checkconditions=True):
    """
    text - start message text
    texterr - error text
    conditions - условия
    check - подтверждение
    checkconditions - checkconditions
    """
    if texterr == None:
        texterr = 'Error!!! ' + text
    while True:
        value = input(f'{text}')
        if checkconditions:
            while value not in conditions:
                value = input(f'{texterr}')
        if check:
            valuecheck = input(f'Your value is - {value}. Are you sure ? (Y)es/(N)o :')
            if valuecheck in [*'Yy'] and valuecheck != '':
                return value
        else:
            return value


def table(func):
    def wrapper(title: str, bottom_line: str, data):
        length = 90
        print(''.center(length, '-'))
        print('|', (title).center(length - 2), '|', sep='')
        print(''.center(length, '-'))
        func(data)
        print(''.center(length, '-'))
        print('|', (bottom_line).center(length - 2), '|', sep='')
        print(''.center(length, '-'))

    return wrapper


@table
def show_list(lit: list):
    for i in range(len(lit)):
        print('|', str(i + 1).center(3), '- ', lit[i].ljust(38), sep='', end='')
        if i % 2 == 1 and i != 0:
            print(' |')
    print()


@table
def show_dict(dct: dict):
    for el in dct:
        print('| ', el.ljust(15), ' - ', str(dct[el]).ljust(68), ' |', sep='')


def user_select(name: str = None) -> dict:
    if name == None:
        while True:
            show_list('Users list',
                      f" (a)dd User, (d)elete User  or  E(x)it     File's format - '{user.strategy()}' - (C)hange",
                      user.strategy.userslist())
            action = set_and_val(
                'Enter user number, or command :',
                [*list(map(str, range(1, len(user.strategy.userslist()) + 1))), *'aAdDxXCc'],
            )
            if action in 'cC':
                strategy = set_and_val(
                    f'Enter files format {list(map(lambda x: x[1:], Files.extensions))}',
                    list(map(lambda x: x[1:], Files.extensions)))
                if strategy == 'json':
                    user.strategy = JsonFile
                if strategy == 'csv':
                    user.strategy = CsvFile
            if action in 'aA':
                if user.readonly:
                    input('!!!Operation is prohibited!!! Press Enter')
                else:
                    name = set_and_val("Enter the name of the new user :", check=True, checkconditions=False)
                    user.strategy.adduser(name)
            if action in 'dD':
                if user.readonly:
                    input('!!!Operation is prohibited!!! Press Enter')
                else:
                    name = set_and_val("Enter the name NUMBER to delete :",
                                       [*list(map(str, range(1, len(user.strategy.userslist()) + 1)))],
                                       check=True)
                    user.strategy.deluser(user.strategy.userslist()[int(name) - 1])
            if action in 'xX':
                exit()
            if action in [*list(map(str, range(1, len(user.strategy.userslist()) + 1)))]:
                return {'user': user.strategy.userslist()[int(action) - 1], 'strategy': user.strategy}
    elif name in user.strategy.userslist():
        return {'user': name, 'strategy': user.strategy}
    else:
        user.strategy.adduser(name)
        return {'user': name, 'strategy': user.strategy}


@table
def show_tasks_table(lst: list) -> None:
    print('|', '#'.center(3), '- ', sep='', end='')
    print('Task name'.center(48), sep='', end='')
    print('Created'.center(10), '  ', sep='', end='')
    print('Deadline'.center(10), '  ', sep='', end='')
    print('Status'.center(11), sep='', end='')
    print('|')
    for num, el in enumerate(lst):
        if el['done']:
            status = 'completed'
        else:
            status = 'in progress'
        print('|', str(num + 1).center(3), '- ', sep='', end='')
        print(el['name'][0:48].ljust(48), sep='', end='')
        print(el['created'].ljust(10), '  ', sep='', end='')
        print(el['deadline'].center(10), '  ', sep='', end='')
        print(status.center(11), sep='', end='')
        print('|')


def show_tasks(lst: list) -> None:
    show_tasks_table('Task list', 'You can do it all!', lst)


def show_task_det(lst: list) -> None:
    flag = True
    while flag:
        show_tasks_table('Task list', 'Choose one! or E(x)it', lst)
        action = set_and_val('Enter task NUMBER :', list(map(str, [*range(1, len(lst) + 1), *'xX'])))
        if action in 'xX':
            break
        for el in lst:
            if lst[int(action) - 1]['counter'] == el['counter']:
                show_dict(f'Task name - "{el["name"]}"', '', el)
        action = input('Do you want to see another Task ? (Y)es or Enter :')
        if action not in 'yY' or action == '':
            flag = False


def add_task(lst: list) -> None:
    flag = True
    while flag:
        newtask = {}
        for el in Task.att2create():
            newtask[el[0]] = input(f'Enter {el[1]} :')
        show_dict(f'Task name - "{newtask["name"]}"', '', newtask)
        action = input('This is right? ? (Y)es or Enter :')
        if action in 'yY':
            flag = False
    user.addtask(**newtask)


def edit_task(lst: list) -> None:
    show_tasks_table('Task list', 'Select a task to edit', lst)
    action = set_and_val('Enter task NUMBER :', list(map(str, [*range(1, len(lst) + 1)])))
    for el in lst:
        if lst[int(action) - 1]['counter'] == el['counter']:
            show_dict(f'Task name - "{el["name"]}"', '', el)
            counter = el['counter']
    key = set_and_val('Enter the key :', user.task_list[0].__dict__.keys())
    value = set_and_val('Enter new text/value', checkconditions=False, check=True)
    user.edittask(counter, **{key: value})


def delete_task(lst: list) -> None:
    show_tasks_table('Task list', 'Select a task to delete', lst)
    nums = input('Enter task NUMBER or NUMBERS (num1,num2,...):')
    nums = list(map(int, nums.replace(' ', '').split(sep=',')))
    counters = []
    for el in lst:
        for i in nums:
            if lst[int(i) - 1]['counter'] == el['counter']:
                counters.append(el['counter'])
    action = input(f'Do you want to delete {user.shownames(*counters)}? (Y)es or Enter')
    if action in 'yY' and action != '':
        user.deltasks(*counters)


def search_task(lst: list) -> None:
    text = input('Enter text to search for all keys or Enter to search for a single key :')
    key = '*'
    if text == '':
        key = set_and_val(f'Enter key "{", ".join(user.task_list[0].__dict__.keys())}" :',
                          user.task_list[0].__dict__.keys())
        text = input('Enter text to search')
    show_task_det(user.filter(text, key))


def sort_task(lst: list) -> None:
    key = set_and_val(f'Enter sorting key "{", ".join(user.task_list[0].__dict__.keys())}" :',
                      user.task_list[0].__dict__.keys())
    show_tasks_table(f'Sorted Task list by {key}', f'--{key}--', user.sorted(key))


def done_task(lst: list) -> None:
    show_tasks_table('Task list', 'Select a task to mark', lst)
    nums = input('Enter task NUMBER or NUMBERS (num1,num2,...):')
    nums = list(map(int, nums.replace(' ', '').split(sep=',')))
    counters = []
    for el in lst:
        for i in nums:
            if lst[int(i) - 1]['counter'] == el['counter']:
                counters.append(el['counter'])
    action = input(f'Do you want to mark {user.shownames(*counters)} as completed? (Y)es or Enter')
    if action in 'yY' and action != '':
        user.taskdone(*counters)


@click.command()
@click.option('-n', 'name', help="user's file name in ./users/ (without extension)")
@click.option('-type', 'strategy', help="file's format (json; csv). Default = json")
@click.option('-r/-w', 'r__o', default=False, help="r - for read-only mode")
def main(name: str = None, r__o: bool = False, strategy=None):
    if strategy == None:
        strategy = JsonFile
    elif strategy in ('JSON', 'json'):
        strategy = JsonFile
    elif strategy in ('CSV', 'csv'):
        strategy = CsvFile
    global user
    user = Tasks(readonly=r__o, strategy=strategy)  # костыль. Т.к. user_select обращается к экземпляру Tasks
    user = Tasks(**user_select(name), readonly=r__o)
    while True:
        show_list('LIST OF TASKS' + chr(174),
                  ' L(O)GOUT - Change user    or     E(x)it ',
                  [func_list[x][1] for x in func_list.keys()])
        action = set_and_val('Enter num of operation :',
                             [*func_list.keys(), *'xXoO'])
        if action in 'xX':
            if not user.readonly:
                user.strategy.safetasks(user.user, user.tasks2save())
            exit()
        if action in 'oO':
            if not user.readonly:
                user.strategy.safetasks(user.user, user.tasks2save())
            user = Tasks(**user_select(), readonly=r__o, strategy=strategy)
        if action in func_list.keys():
            func_list[action][0](user.showtasks(False))
        input('Press Enter to continue')


func_list = {'1': (show_tasks, 'Show tasks list'),
             '2': (show_task_det, 'Show task details'),
             '3': (add_task, 'Add task'),
             '4': (edit_task, 'Edit task'),
             '5': (delete_task, 'Delete task'),
             '6': (search_task, 'Search for a task'),
             '7': (sort_task, 'Display sorted list'),
             '8': (done_task, 'Mark task as completed'),
             }

main()
