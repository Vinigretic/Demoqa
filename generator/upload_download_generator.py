import csv
import json
import os
import random
import tempfile


# The tempfile module from the Python standard library allows:
# - Create unique temporary files and folders
# - Work with them like regular files
# - Automatically manage their deletion (if needed)
# - Avoid name conflicts and manual path specifications


# def generator_file():
#     path = rf"C:\Users\vbaka\PycharmProjects\Demoqa\filetest{random.randint(0, 999)}.txt"
#     file = open(file=path, mode="w", encoding="utf-8")
#     file.write(f'Hello World!\n{random.randint(0, 999)}\n')
#     file.close()
#     return file.name, path


class FileFactory:
    # NamedTemporaryFile - this is a function from the tempfile module that creates a temporary file with a unique name
    # that is accessible on disk. exc - C:\Users\vbaka\AppData\Local\Temp\tmpsf37xm6u.txt

    @staticmethod
    def create_temp_txt(content=None):
        content = content or f"Hello World!\n{random.randint(0, 999)}"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as file:
            file.write(content)
            return file.name

    @staticmethod
    def create_temp_json(data=None):
        data = data or {"message": "Hello", "id": random.randint(0, 999)}
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as file:
            json.dump(data, file)
            return file.name

    @staticmethod
    def create_temp_csv(rows=None):
        rows = rows or [["Name", "Age"], ["Alice", "30"], ["Bob", str(random.randint(20, 40))]]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
            return file.name

    @staticmethod
    def delete_file(path):
        if os.path.exists(path):
            os.remove(path)
