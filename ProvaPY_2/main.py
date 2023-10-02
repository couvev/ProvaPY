import pandas as pd
import time
import matplotlib.pyplot as plt

caminho_excel = "folha_pag.xlsx"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

try:
    df = pd.read_excel(caminho_excel)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Nome', 'Cargo', 'Salario', 'Horas_Trabalhadas'])

def main():
    selec = 0

    while selec != 10:
        selec = int(input("\nDigite o número da opção desejada:\n\n"
                          "1. Adicionar cadastro\n"
                          "2. Imprimir cadastros\n"
                          "3. Imprimir cadastros com IR\n"
                          "4. Apagar cadastro\n"
                          "10. Sair\n\n"))

        if selec == 1:
            cadastrar_funcionario()
            time.sleep(4)

        elif selec == 2:
            imprimir_cadastros(caminho_excel)
            time.sleep(4)

        elif selec == 3:
            imposto_renda(caminho_excel)
            time.sleep(4)

        elif selec == 4:
            apagar_cadastro(caminho_excel)
            time.sleep(4)

    print("Programa encerrado.")

class Funcionario:
    def __init__(self, nome, cargo, salario, horas_trabalhadas):
        self.nome = nome
        self.cargo = cargo
        self.salario = salario
        self.horas_trabalhadas = horas_trabalhadas

def cadastrar_funcionario():
    nome = input("Digite o nome do funcionário: ")
    cargo = input("Digite o cargo do funcionário: ")
    salario = float(input("Digite o salário do funcionário: "))
    horas_trabalhadas = float(input("Digite o número de horas trabalhadas: "))

    novo_funcionario = Funcionario(nome, cargo, salario, horas_trabalhadas)
    df = pd.read_excel('folha_pag.xlsx')

    nova_linha = pd.DataFrame([[novo_funcionario.nome, novo_funcionario.cargo, novo_funcionario.salario, novo_funcionario.horas_trabalhadas]],
                               columns=['Nome', 'Cargo', 'Salario', 'Horas_Trabalhadas'])
    df = pd.concat([df, nova_linha], ignore_index=True, sort=False)

    df.to_excel('folha_pag.xlsx', index=False)

    print("\nFuncionário cadastrado com sucesso e adicionado ao arquivo Excel!\n")

def imprimir_cadastros(caminho_excel):
    
    df = pd.read_excel(caminho_excel)
    
    if not df.empty:
        print(df)
    else:
        print("Nenhum cadastro encontrado.")

def imposto_renda(caminho_excel):
    
    df = pd.read_excel(caminho_excel)

    df['Liquido'] = 0
    df['Desconto'] = 0

    for indice, linha in df.iterrows():
        salario = linha['Salario']
        
        if salario <= 1500:
            df.at[indice, 'Liquido'] = salario
            
        elif 1500 < salario < 3000:
            df.at[indice, 'Liquido'] = salario * 0.85
            df.at[indice, 'Desconto'] = salario * 0.15
        
        elif 3000 < salario < 5000:
            df.at[indice, 'Liquido'] = salario * 0.80
            df.at[indice, 'Desconto'] = salario * 0.20
        
        elif 5000 < salario:
            df.at[indice, 'Liquido'] = salario * 0.73
            df.at[indice, 'Desconto'] = salario * 0.27
        
    print(df)
    df.to_excel(caminho_excel, index=False)

def apagar_cadastro(caminho_excel):
    df = pd.read_excel(caminho_excel)
    
    print(df)
    time.sleep(4)
    exc = int(input("Selecione qual você quer excluir pelo indice: "))
    
    df = df.drop(exc)
    
    print("Cadastros atualizados: \n\n")
    print(df)

    df.to_excel(caminho_excel, index=False)

if __name__ == "__main__":
    main()