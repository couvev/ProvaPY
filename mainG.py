import pandas as pd
import tkinter as tk
from tkinter import ttk

caminho_excel = "folha_pag.xlsx"

class Funcionario:
    def __init__(self, nome, cargo, salario, horas_trabalhadas):
        self.nome = nome
        self.cargo = cargo
        self.salario = salario
        self.horas_trabalhadas = horas_trabalhadas

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Folha de Pagamento")
    
        self.root.geometry("600x500") 
        
        self.root.resizable(False, False)
        
        # Adiconando Icone
        self.root.iconbitmap("icon.ico")
        
        self.tabControl = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text="Cadastrar")
        self.tabControl.add(self.tab2, text="Imprimir Cadastros")
        self.tabControl.add(self.tab3, text="Imposto de Renda")
        self.tabControl.add(self.tab4, text="Apagar Cadastro")

        self.tabControl.pack(expand=1, fill="both")

        # Variaveis de entrada
        self.nome_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        self.salario_var = tk.IntVar()
        self.horas_var = tk.IntVar()
        self.delete_var = tk.StringVar()

        # Output
        self.output_text = tk.Text(self.root, height=20, width=80, wrap="word", state="disabled")
        self.output_text.pack(padx=10, pady=10)

        self.limpar_output() 

        # Tab 1: Cadastrar
        tk.Label(self.tab1, text="Nome:").grid(row=0, column=5, padx=5, pady=5, sticky="e")
        tk.Entry(self.tab1, textvariable=self.nome_var).grid(row=0, column=6, padx=5, pady=5, sticky="w", columnspan=2)

        tk.Label(self.tab1, text="Cargo:").grid(row=1, column=5, padx=5, pady=5, sticky="e")
        tk.Entry(self.tab1, textvariable=self.cargo_var).grid(row=1, column=6, padx=5, pady=5, sticky="w", columnspan=2)

        tk.Label(self.tab1, text="Salário:").grid(row=2, column=5, padx=5, pady=5, sticky="e")
        tk.Entry(self.tab1, textvariable=self.salario_var).grid(row=2, column=6, padx=5, pady=5, sticky="w", columnspan=2)

        tk.Label(self.tab1, text="Horas Trabalhadas:").grid(row=3, column=5, padx=5, pady=5, sticky="e")
        tk.Entry(self.tab1, textvariable=self.horas_var).grid(row=3, column=6, padx=5, pady=5, sticky="w", columnspan=2)

        tk.Button(self.tab1, text="Cadastrar", command=self.cadastrar_funcionario).grid(row=4, column=5, padx=5, pady=5, columnspan=3, sticky="ew")

        
        # Tab 2: Imprimir Cadastros
        tk.Button(self.tab2, text="Imprimir Cadastros", command=self.imprimir_cadastros).pack(pady=20)
        
        # Tab 3: Imposto de Renda
        tk.Button(self.tab3, text="Calcular Imposto de Renda", command=self.imposto_renda).pack(pady=20)
        
        # Tab 4: Apgar cadastro
        tk.Label(self.tab4, text="ID que deseja apagar:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.tab4, textvariable=self.delete_var).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.tab4, text="Apagar Cadastro", command=self.apagar_cadastro).grid(row=1, column=0, columnspan=2, pady=20)


    def limpar_output(self):
        """Limpa o conteúdo do widget de texto."""
        self.output_text.config(state="normal")  # Habilita a edição
        self.output_text.delete(1.0, tk.END)  # Deleta todo o texto
        self.output_text.config(state="disabled")  # Desabilita a edição

    def cadastrar_funcionario(self):
        nome = self.nome_var.get()
        cargo = self.cargo_var.get()
        salario = self.salario_var.get()
        horas_trabalhadas = self.horas_var.get()
        
        self.limpar_output()

        if nome == "" or cargo == "" or salario < 0.1 or horas_trabalhadas < 0.1:
            self.output_text.config(state="normal")
            self.output_text.insert(tk.END, "\nAdicione todas as informações!\n")
            self.output_text.config(state="disabled")
            
        else:
            df = pd.read_excel('folha_pag.xlsx')
            
            novo_funcionario = Funcionario(nome, cargo, salario, horas_trabalhadas)

            nova_linha = pd.DataFrame([[novo_funcionario.nome, novo_funcionario.cargo, novo_funcionario.salario,
                                        novo_funcionario.horas_trabalhadas]],
                                    columns=['Nome', 'Cargo', 'Salario', 'Horas_Trabalhadas'])
            df = pd.concat([df, nova_linha], ignore_index=True, sort=False)

            df.to_excel('folha_pag.xlsx', index=False)

            self.output_text.config(state="normal")
            self.output_text.insert(tk.END, "\nFuncionário cadastrado com sucesso e adicionado ao arquivo Excel!\n")
            self.output_text.config(state="disabled")

    def imprimir_cadastros(self):
        df = pd.read_excel(caminho_excel)
        
        self.limpar_output()
        
        self.output_text.config(state="normal")

        if not df.empty:
            self.output_text.insert(tk.END, "\n" + df.to_string(index=False) + "\n")
        else:
            self.output_text.insert(tk.END, "\nNenhum cadastro encontrado.\n")
        self.output_text.config(state="disabled")

    def imposto_renda(self):
        
        self.limpar_output()
        
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
            
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, "\n" + df.to_string(index=False) + "\n")
        self.output_text.config(state="disabled")
        df.to_excel(caminho_excel, index=False)

    def apagar_cadastro(self):
        nome = self.delete_var.get()
        
        self.limpar_output()
        
        df = pd.read_excel(caminho_excel)
        
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, "\n" + df.to_string(index=False) + "\n")
        
        if nome in df['Nome'].values:
            df = df[df['Nome'] != nome]
            self.output_text.insert(tk.END, "\nCadastro de '{}' removido com sucesso.\n".format(nome))
        else:
            self.output_text.insert(tk.END, "\nNão foi possível encontrar o cadastro de '{}'.\n".format(nome))
        
        self.output_text.insert(tk.END, "\nCadastros atualizados: \n\n" + df.to_string(index=False) + "\n")
        self.output_text.config(state="disabled")

        df.to_excel(caminho_excel, index=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()