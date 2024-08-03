import mysql.connector

# Classe para estabelecer conexão com banco de dados
class ConexaoBancoDeDados:
    def __init__(self, host, hostname, password, database) -> None:
        self._host = host
        self._hostname = hostname
        self._password = password
        self._database = database
        self.MYDB = None

    def __enter__(self):
        self.MYDB = mysql.connector.connect(
            host = self._host,
            user = self._hostname,
            password = self._password,
            database = self._database
        )
        return self.MYDB
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.MYDB.close()

# Operações básicas no banco de dados Mysql
class OperacaoMysql:
    def __init__(self, mybd) -> None:
        self._mydb = mybd
        self._cursor = self._mydb.cursor()

    # Adição de novo usuário
    def adicao_novo_usuario(self, usuario:dict) -> bool:
        sintaxe = 'INSERT INTO usuarios (nome, nick, senha) VALUES (%s, %s, %s)'
        
        self._cursor.execute(sintaxe, tuple(usuario.values()))
        self._mydb.commit()
        linha_afetadas = self._cursor.rowcount
        return False if linha_afetadas <= 0 else True
    
    # Adição de novos registros de alterações
    def novo_registro(self, registros:dict) -> bool:
        sintaxe = 'INSERT INTO operacao (id_user, campo, dado_antigo, dado_novo) VALUES (%s, %s, %s, %s)'
        self._cursor.execute(sintaxe, tuple(registros.values()))
        self._mydb.commit()
        linha_afetadas = self._cursor.rowcount
        return False if linha_afetadas <= 0 else True
    
    # Atualizar usuário, com o campo que deseja alterar e o id
    def atualizar_usuario(self, usuario:tuple, campo:str) -> bool:
        sintaxe = f'UPDATE usuarios SET {campo} = %s WHERE id = %s'
        
        self._cursor.execute(sintaxe, usuario)
        self._mydb.commit()
       
        return None

    # Listar todos os usuários armazenados no banco de dados
    @property
    def listar_usuarios(self) -> list[str]:
        sintaxe = 'SELECT * FROM usuarios'
        
        self._cursor.execute(sintaxe)
        return self._cursor.fetchall()
    
    #Listar todas as alterações que foram realizadas no banco de dados
    @property
    def listar_alteracao(self) -> list[str]:
        sintaxe = 'SELECT * FROM operacao'
        
        self._cursor.execute(sintaxe)
        return self._cursor.fetchall()
    
    # Remover o usuário por meio de seu id
    def remover_usuario(self, usuario_id: tuple) -> bool:
        sintaxe = 'DELETE FROM usuarios WHERE id = %s'
        
        self._cursor.execute(sintaxe, usuario_id)
        self._mydb.commit()
        linha_afetadas = self._cursor.rowcount
        return False if linha_afetadas <= 0 else True
    
    # Apagar todos os registros da tabela
    def apagar_usuarios(self):
        sintaxe = 'TRUNCATE TABLE usuarios'
        
        self._cursor.execute(sintaxe)
        self._mydb.commit()
        linha_afetadas = self._cursor.rowcount
        return False if linha_afetadas <= 0 else True
    
    # Procurar um determinado usuário
    def procurar_usuario(self, id_):
        sintaxe = 'SELECT * from usuarios WHERE id = %s'
        self._cursor.execute(sintaxe, (id_,))
        try:
            dado = self._cursor.fetchall()[0]
            
            return  {
                    'id': dado[0],
                    'nome': dado[1],
                    'nick': dado[2],
                    'senha': dado[3]
                }
        except IndexError:
            return True

if __name__ == '__main__':
    CONEXAO = ConexaoBancoDeDados(
        host='localhost',
        hostname='root',
        password='1234',
        database='crud'
    )
    with CONEXAO as mysql:
        operacao = OperacaoMysql(mybd=mysql)
        print(operacao.remover_usuario((78,)))