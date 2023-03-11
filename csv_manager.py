import csv


class CSV():
    def __init__(self, file_name):
        self.file_name = file_name
        self.fieldnames = ['id', 'lesson', 'stage']

    def print(self):
        with open(self.file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)

    def write(self, data):
        # проверяем, есть ли запись с таким именем
        if self.check(data['id']):
            # если есть, обновляем существующую запись
            rows = []
            with open(self.file_name, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['id'] == data['id']:
                        rows.append(data)
                    else:
                        rows.append(row)
            with open(self.file_name, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        else:
            # если нет, добавляем новую запись
            with open(self.file_name, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)

    def read(self, name):
        with open(self.file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == name:
                    return row
        return None

    def check(self, name):
        with open(self.file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == name:
                    return True
        return False
