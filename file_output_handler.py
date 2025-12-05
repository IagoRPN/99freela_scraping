import json

class FileHandler():
    def __init__(self, filename: str):
        self.filename = filename

        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write("Palavra-Chave,Titulo do Projeto, Link, Descrição\n")

    def save_to_file(self, data: list):
        with open(self.filename, 'a', encoding='utf-8') as file:
            for item in data:
                file.write(f"{json.loads(item).get("keyword")},{json.loads(item).get("title")},{json.loads(item).get("link")},{json.loads(item).get("description")}\n")