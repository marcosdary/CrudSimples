from banco_de_dados import OperacaoMysql, ConexaoBancoDeDados
import os

CONEXAO = ConexaoBancoDeDados(
    host='localhost',
    hostname='root',
    password='1234',
    database='crud'
)

class Main:
    def __init__(self, operacao) -> None:
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

    def atualizar_usuario(self):
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
                self.atualizar_usuario()

        id_usuario = input('\nID: ')
        novo_valor = input('Valor: ')
        print(
            'Status:',            
            'Usuário atualizado com sucesso 😁✌\n' 
            if self.operacao.atualizar_usuario(campo=campo_escolhido, usuario=(novo_valor, id_usuario))
            else 'Problema em atualizar o usuário 😑😐\n'
        )
with CONEXAO as mysql:
    operacao = OperacaoMysql(mybd=mysql) 
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
            7.                  SAIR
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
                main.atualizar_usuario()

            case '5':
                operacao.apagar_usuarios()

            case '7':
                print(
                    '''
                        OBRIGADO PELA ATENÇÃO VOLTE SEMPRE ;) ^_~
                    '''
                )
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
                