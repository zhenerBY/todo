import json
import csv


def opentasks(name) -> None:
    global task_list
    task_list = []
    with open(name + '.json', 'r') as file_json:
        task_list = json.load(file_json)


def csv_safe():
    with open('test.csv', 'w') as f:
        names = list(task_list[0].keys())
        writer = csv.DictWriter(f, fieldnames=names)
        writer.writeheader()
        for line in task_list:
            writer.writerow(line)

def csv_open():
    global csv_list
    csv_list=[]
    with open('test.csv', 'r') as f:
        file_reader = csv.DictReader(f)
        for row in file_reader:
            csv_list.append(row)



opentasks('Test_user')