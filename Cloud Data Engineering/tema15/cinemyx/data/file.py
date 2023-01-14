import csv
from genericpath import exists
from os import path, mkdir, remove
from pathlib import Path

class File:

    def __init__(self) -> None:
        self.data = Path(path.dirname(__file__))

    def data_path(self, sub_dir = None, file_name = None) -> str:
        if not sub_dir: return self.data
        if not file_name: full_path = path.join(self.data, sub_dir)
        else: full_path = path.join(self.data, sub_dir, f'{file_name}.csv')
        if not exists(path.join(self.data, sub_dir)): mkdir(path.join(self.data, sub_dir))
        if not exists(full_path): mkdir(full_path)
        return full_path

    def delete(self, sub_dir: str, file_name: str):
        full_path = path.join(self.data, sub_dir, f'{file_name}.csv')
        if exists(full_path): remove(full_path)

class Write(File):

    def write(self, file_name, rows, sub_dir, file_name_dir = False) -> None:
        if file_name_dir:
            full_path = path.join(super().data_path(sub_dir = sub_dir, file_name = file_name), f'{file_name}.csv')
        else:
            full_path = path.join(super().data_path(sub_dir = sub_dir), f'{file_name}.csv')
        with open(full_path, mode = 'w', encoding = 'utf-8', newline = '') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerows(rows)

    def append(self, file_name, row, sub_dir, file_name_dir = False) -> None:
        if file_name_dir:
            full_path = path.join(super().data_path(sub_dir = sub_dir, file_name = file_name), f'{file_name}.csv')
        else:
            full_path = path.join(super().data_path(sub_dir = sub_dir), f'{file_name}.csv')
        with open(full_path, mode = 'a', encoding = 'utf-8', newline = '') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(row)

class Read(File):

    def read(self, file_name, sub_dir, file_name_dir = False) -> list:
        if file_name_dir:
            full_path = path.join(super().data_path(sub_dir = sub_dir, file_name = file_name), f'{file_name}.csv')
        else:
            full_path = path.join(super().data_path(sub_dir = sub_dir), f'{file_name}.csv')
        if not exists(full_path):
            with open(full_path, mode = 'w', encoding = 'utf-8', newline = '') as file:
                file.close()
        file = open(full_path, mode = 'r', encoding = 'utf-8')
        rows = csv.reader(file)
        return rows