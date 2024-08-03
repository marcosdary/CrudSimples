from banco_de_dados import OperacaoMysql, ConexaoBancoDeDados
from backup import OperacaoJson, FILE_JSON
import os

CONEXAO_CRUD = ConexaoBancoDeDados(
    host='localhost',
    hostname='root',
    password='1234',
    database='crud'
)

class Main:
    def __init__(self, operacao:OperacaoMysql) -> None:
        self.operacao = operacao
    def novo_usuario(self):
        
        print(
            '''
                        DADOS DO NOVO USUÁRIO
            '''
        )
        dict_ = {}
        dict_['nome'] = input('Nome: ')
        dict_['nick'] = input('Nick: ')
        dict_['senha'] = input('Password: ')
        print(
                'Status:',
                'Usuário adicionado com sucesso 😁✌\n' if self.operacao.adicao_novo_usuario(dict_)
                else 'Problema em adicionar o usuário 😑😐\n'
            )
        
    def remover_usuario(self):
        while True:
            id_usuario = input('ID: ')
            if id_usuario.isnumeric():
                print(
                    'Status:',
                    'Usuário removido com sucesso 😁✌\n' if  self.operacao.remover_usuario((id_usuario,)) 
                    else 'Problema em remover o usuário 😑😐\n'
                )
                break
            else:
                print(
                    '''

                            ID INVÁLIDO 🙁

                    '''
                )
            
    def listar_usuarios(self):
        os.system('cls')
        print(f'{"ID":<20} {"NOME":<30} {"NICK":<20} {"PASSWORD"}')
        for user in self.operacao.listar_usuarios:
            print(f'{user[0]:<20} {user[1]:<30} {user[2]:<20} {user[3]}')

    def listar_atualizacao_recentes(self):
        os.system('cls')
        print(f'{"ID":<20} {"ID USER":<30} {"CAMPO":<20} {"DADO ALTERADO":<20} {"NOVO DADO":<20} {"DATA E HORA"}')
        for registro in self.operacao.listar_alteracao:
            print(f'{registro[0]:<20} {registro[1]:<30} {registro[2]:<20} {registro[3]:<20} {registro[4]:<20} {registro[5]}')
        
    def atualizar_usuario(self, arquivo_json:list):
        print(
            '''
                    -------------------------------
                    CAMPO PARA ATUALIZAR INFORMAÇÃO

                    1.                          NOME
                    2.                          NICK
                    3.                         SENHA
                    --------------------------------
            '''
        )
        campo = input(
             '''    
                    Opção de campo: '''
        )
        campo_escolhido = ''

        match campo:
            case '1':
                campo_escolhido = 'nome'
            case '2':
                campo_escolhido = 'nick'
            case '3':
                campo_escolhido = 'senha'
            case _:
                print(
                    """

                            ESCOLHA UMA DAS OPÇÕES 🙄😑

                    """
                )
                return self.atualizar_usuario(arquivo_json)
        id_usuario = input('\nID: ')
        dado_user = self.operacao.procurar_usuario(id_usuario)
        
        if not isinstance(dado_user, dict):
            print(
                  '''
                  Status
                        Problema em atualizar o usuário 
                        Verifique que o id é igual😑😐
                  '''
            )
            return self.atualizar_usuario(arquivo_json)

        novo_valor = input('Valor: ')
        dict_ = {
            'id': dado_user['id'],
            'campo': campo_escolhido, 
            'dado_antigo': dado_user[f'{campo_escolhido}'],
            'dado': novo_valor
        }
        print(
            'Status:',            
            'Usuário atualizado com sucesso 😁✌\n'   
        )
        self.operacao.atualizar_usuario(campo=campo_escolhido, usuario=(novo_valor, id_usuario))
        arquivo_json.append(dict_)
        return arquivo_json
    
    def salvar_alteracao(self, registros:dict):
        if registros == []:
            return True
        for registro in registros:
            if not self.operacao.novo_registro(registro):
                raise ValueError("Backup não foi realizado")
        return True

with CONEXAO_CRUD as mysql:
    operacao = OperacaoMysql(mybd=mysql) 
    opp = OperacaoJson()
    arquivo_json = opp.jsonread([])
    
    while True:
        print(
        '''
            ------------------------------------------------------------------
                                TELA INICIAL
        
            1.                  ADICIONAR NOVO USUÁRIO
            2.                  REMOVER USUÁRIO
            3.                  EXIBIR USUÁRIOS
            4.                  ATUALIZAR INFORMAÇÕES DO USUÁRIO
            5.                  APAGAR TODOS OS USUÁRIOS
            6.                  LIMPA TERMINAL
            7.                  ALTERAÇÕES REALIZADAS NOS USUÁRIOS
            8.                  SAIR
            ------------------------------------------------------------------
        '''
        )
        opcao = input(
        ''' 
            opção: '''
        )
        main = Main(operacao)
        match opcao:
            case '1':
                main.novo_usuario()

            case '2':
                main.remover_usuario()

            case '3':
                main.listar_usuarios()

            case '4':
                lista = main.atualizar_usuario(arquivo_json)
                opp.jsonwrite(lista)

            case '5':
                operacao.apagar_usuarios()

            case '7':
                main.listar_atualizacao_recentes()

            case '8':
                print(
                    '''
                        OBRIGADO PELA ATENÇÃO VOLTE SEMPRE ;) ^_~
                    '''
                )
                main.salvar_alteracao(arquivo_json)
                print(
                    '''
                                        Backup realizado com sucesso....
                    '''
                )
                os.remove(FILE_JSON)
                break
            
            case '6':
                os.system('cls')
            case _:
                print(
                    '''
                        OPÇÃO INVÁLIDA 🤨🙁
                        ESCOLHA UMA DAS OPÇÕES
                    '''
                )
                