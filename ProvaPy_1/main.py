import pandas as pd
import time
import matplotlib.pyplot as plt

def calcular_faturamento(planilha):
    faturamento_total = 0

    for _, linha in planilha.iterrows():
        preco = linha['Preco']
        venda = linha['Venda']

        if isinstance(preco, (int, float)) and isinstance(venda, (int, float)):
            faturamento_total += preco * venda

    return faturamento_total

def fatu_ind(planilha):
    novo_planilha = planilha.copy()  
    novo_planilha['Fat'] = (planilha['Preco'] * planilha['Venda'])
    return novo_planilha.iloc[:, 2:6]

def calcular_porcentagem(planilha):
    faturamento_total = calcular_faturamento(planilha)
    novo_planilha = planilha.copy()  
    novo_planilha['Porcentagem'] = (planilha['Preco'] * planilha['Venda']) / faturamento_total * 100
    return novo_planilha.iloc[:, 2:6]

def plotar_grafico_mais_vendidos(planilha, n):
    faturamento_total = calcular_faturamento(planilha)
    
    planilha['Porcentagem'] = (planilha['Preco'] * planilha['Venda']) / faturamento_total * 100
    
    vendas_por_mercadoria = planilha.groupby('Item')['Porcentagem'].sum()

    top_mais_vendidos = vendas_por_mercadoria.nlargest(n)

    top_mais_vendidos.plot(kind='bar', color='skyblue')
    plt.xlabel('Mercadorias')
    plt.ylabel('Porcentagem em relação ao faturamento total')
    plt.title(f'As {n} Mercadorias Mais Vendidas')

    plt.show()
    
def exportar_para_txt(planilha, nome_arquivo_txt):
    try:
        planilha.to_csv(nome_arquivo_txt, sep='\t', index=False)
        print(f"Planilha exportada com sucesso para {nome_arquivo_txt}")
    except Exception as e:
        print(f"Erro ao exportar a planilha: {e}")

def main():
    caminho_excel = "base.xlsx"
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    planilha = pd.read_excel(caminho_excel)

    selec = 0  

    while selec != 10:
        selec = int(input("\nDigite o número da opção desejada:\n"
                          "1. Ver faturamento total\n"
                          "2. Ver faturamento individual\n"
                          "3. Ver lista porcentagem sobre o fat. total\n"
                          "4. Gravar os arquivos das vendas em um TXT\n"
                          "5. Gráfico dos itens mais vendidos\n"
                          "10. Sair\n"))

        if selec == 1:
            print(f"\nFaturamento total: R${calcular_faturamento(planilha)}")
            time.sleep(2)
        
        elif selec == 2:
            print(fatu_ind(planilha))
            time.sleep(3)
            
        elif selec == 3:
            print(calcular_porcentagem(planilha))
            time.sleep(3)
            
        elif selec == 4:
            nome_dese = input("Qual sera o nome do TXT? ")
            time.sleep(1)
            exportar_para_txt(planilha, nome_dese)
            time.sleep(3)
        
        elif selec == 5:
            qnt_dese = int(input("Quantos itens deseja no grafico? "))
            print(plotar_grafico_mais_vendidos(planilha, qnt_dese))
            time.sleep(3)

    print("Programa encerrado.")

if __name__ == "__main__":
    main()
