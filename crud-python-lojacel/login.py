import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from tkinter import simpledialog
import tkinter.scrolledtext as scrolledtext


class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ICONCELL LOGIN")
        self.geometry("400x200")

        self.label_user = tk.Label(self, text="Usuário:")
        self.label_user.pack(pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.pack(pady=5)

        self.label_password = tk.Label(self, text="Senha:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=15)

    def login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()

        # Verificar usuário e senha (simulação simples)
        if user == "admin" and password == "admin":
            self.destroy()
            MainScreen()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos")

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ICONCELL OPERAÇÕES")
        self.geometry("400x300")

        # Barra de Menu
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Menu "Operações"
        self.operacoes_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Operações", menu=self.operacoes_menu)
        self.operacoes_menu.add_command(label="Gerir Produtos", command=self.open_crud)
        self.operacoes_menu.add_command(label="Sair", command=self.logout)

    def open_crud(self):
        self.destroy()
        CrudScreen()

    def logout(self):
        self.destroy()
        LoginScreen()

class CrudScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ICONCELL PRODUTOS")
        self.geometry("500x400")

        # Barra de Menu
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Menu "CRUD"
        self.crud_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Gestão de Produtos", menu=self.crud_menu)
        self.crud_menu.add_command(label="Inserir", command=self.insert_data)
        self.crud_menu.add_command(label="Consultar", command=self.query_data)
        self.crud_menu.add_command(label="Consultar Unitário", command=self.query_data_one)
        self.crud_menu.add_command(label="Atualizar", command=self.update_data)
        self.crud_menu.add_command(label="Excluir", command=self.delete_data)
        self.crud_menu.add_command(label="Voltar", command=self.go_back)

       

        # Conectar ao MongoDB
        self.client = MongoClient("mongodb+srv://Onaitsirc:7qqR0HTx9fHdd0tf@iconcell.il7szxn.mongodb.net/iconcell")
        self.db = self.client["celular_db"]
        self.collection = self.db["celulares"]
             

    def insert_data(self):
            marca = simpledialog.askstring("Inserir Dados", "Digite a marca do celular:")
            modelo = simpledialog.askstring("Inserir Dados", "Digite o modelo do celular:")
            ano = simpledialog.askinteger("Inserir Dados", "Digite o ano do celular:")
            cor = simpledialog.askstring("Inserir Dados", "Digite a cor do celular:")
            preco = simpledialog.askfloat("Inserir Dados", "Digite o preço do celular:")

            if marca and modelo and ano and cor and preco is not None:
                data = {"marca": marca, "modelo": modelo, "ano": ano, "cor": cor, "preco": preco}
                self.collection.insert_one(data)
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def query_data(self):
         # Consultar todos os documentos na coleção
        cursor = self.collection.find()

        # Criar uma nova janela para exibir os resultados
        query_window = tk.Toplevel(self)
        query_window.title("Consulta de Dados")
        query_window.geometry("500x300")

        # Criar um widget de texto rolável para exibir os resultados
        text_widget = scrolledtext.ScrolledText(query_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill="both")

        # Adicionar os resultados ao widget de texto
        for document in cursor:
            text_widget.insert(tk.END, f"Marca: {document['marca']}\n")
            text_widget.insert(tk.END, f"Modelo: {document['modelo']}\n")
            text_widget.insert(tk.END, f"Ano: {document['ano']}\n")
            text_widget.insert(tk.END, f"Cor: {document['cor']}\n")
            text_widget.insert(tk.END, f"Preço: {document['preco']}\n")
            text_widget.insert(tk.END, "-"*30 + "\n")
    
    def query_data_one(self):
        modelo_consulta = simpledialog.askstring("Consultar Dados", "Digite o modelo do celular para consultar:")

        if modelo_consulta:
            query = {"modelo": modelo_consulta}
            result = self.collection.find_one(query)

            if result:
                messagebox.showinfo("Resultado da Consulta", f"Marca: {result['marca']}\nModelo: {result['modelo']}\nAno: {result['ano']}\nCor: {result['cor']}\nPreço: {result['preco']}")
            else:
                messagebox.showinfo("Resultado da Consulta", "Nenhum resultado encontrado para o modelo especificado.")

    def update_data(self):
        # Solicitar ao usuário o modelo do celular a ser atualizado
        modelo_atualizar = simpledialog.askstring("Atualizar Dados", "Digite o modelo do celular a ser atualizado:")

        # Verificar se o modelo foi fornecido
        if modelo_atualizar:
            # Solicitar ao usuário os novos dados
            marca = simpledialog.askstring("Atualizar Dados", "Digite a nova marca do celular:")
            ano = simpledialog.askinteger("Atualizar Dados", "Digite o novo ano do celular:")
            cor = simpledialog.askstring("Atualizar Dados", "Digite a nova cor do celular:")
            preco = simpledialog.askfloat("Atualizar Dados", "Digite o novo preço do celular:")

            # Verificar se os novos dados foram fornecidos
            if marca and ano and cor and preco is not None:
                # Critérios de pesquisa para o documento a ser atualizado
                criteria = {"modelo": modelo_atualizar}

                # Novos valores a serem definidos
                new_values = {"$set": {"marca": marca, "ano": ano, "cor": cor, "preco": preco}}

                # Atualizar o documento na coleção
                result = self.collection.update_one(criteria, new_values)

                # Verificar se a atualização foi bem-sucedida
                if result.modified_count > 0:
                    messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Nenhum documento correspondente encontrado para atualizar.")
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        else:
            messagebox.showerror("Erro", "Por favor, forneça o modelo do celular a ser atualizado.")


    def delete_data(self):
       # Solicitar ao usuário o modelo do celular a ser excluído
        modelo_excluir = simpledialog.askstring("Excluir Dados", "Digite o modelo do celular a ser excluído:")

        # Verificar se o modelo foi fornecido
        if modelo_excluir:
            # Critérios de pesquisa para o documento a ser excluído
            criteria = {"modelo": modelo_excluir}

            # Excluir o documento na coleção
            result = self.collection.delete_one(criteria)

            # Verificar se a exclusão foi bem-sucedida
            if result.deleted_count > 0:
                messagebox.showinfo("Sucesso", "Dados excluídos com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Nenhum documento correspondente encontrado para excluir.")
        else:
            messagebox.showerror("Erro", "Por favor, forneça o modelo do celular a ser excluído.")


    def go_back(self):
        self.destroy()
        MainScreen()

if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()
