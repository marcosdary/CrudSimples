import json
import os

CAMINHO = os.path.dirname(__file__)
FILE_JSON = os.path.join(CAMINHO, 'data.json')

class ConexaoJson:

    CAMINHO = os.path.dirname(__file__)
    FILE = os.path.join(CAMINHO, 'data.json')

    def __init__(self, operacao) -> None: 
        self.operacao = operacao
        self.arquivo = None

    def __enter__(self):
        arquivo = open(self.FILE, self.operacao, encoding='utf-8')
        self.arquivo = arquivo
        return self.arquivo
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.arquivo.close()
        if exc_type is not None:
            print(f'{exc_type.__name__}: {exc_value}')
            return True

class OperacaoJson:

    # Operação de leitura | Caso não haja nada, chama-se o método
    #   jsonwrite para que possa criar o arquivo json
    def jsonread(self, data):
        try:
            with ConexaoJson('r') as file:
                return json.load(file)
            
        except FileNotFoundError:
            self.jsonwrite(data)
        return data
    
    # Operação de escrita
    def jsonwrite(self, data):
        with ConexaoJson('w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        


