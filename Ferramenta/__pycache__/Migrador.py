import customtkinter as ctk
from customtkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pymysql
from pymongo import MongoClient
import datetime
from decimal import Decimal
from tkinter import BooleanVar, messagebox
from CTkListbox import *
from PIL import Image, ImageTk

class MigrationApp:
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("800x500")
        self.root.title("Ferramenta Migradora")

        
        ctk.set_appearance_mode("dark")

        master_frame = ctk.CTkFrame(self.root)
        master_frame.pack(fill="both", expand=True)
        
        self.tabview = ctk.CTkTabview(master=master_frame)
        self.tabview.pack(side="left", fill="both", expand=True) 
                
        self.switch_state = ctk.BooleanVar(value=True)
    
        self.tab1 = self.tabview.add("MySQL")
        self.tab2 = self.tabview.add("MongoDB")
        self.tab = self.tabview.add("Migrar")
        
        self.tabviewschema = ctk.CTkTabview(master=self.tab)
        self.tabviewschema.pack(side="left", fill="y")  # Coloca à esquerda e estende-se na direção vertical
        
        self.tab1view2 = self.tabviewschema.add("MysqlSchema")
        self.tab2view2 = self.tabviewschema.add("MongoDBSchema")
        
        self.listbox_tables = CTkListbox(self.tab1view2)
        self.listbox_tables.pack(fill="both", expand=True)
        
        
        self.listbox_tables_mongo = CTkListbox(self.tab2view2)
        self.listbox_tables_mongo.pack(fill="both", expand=True)
        
        self.icon = Image.open('mysql.png')
        
        # Redimensionar a imagem para um tamanho adequado (por exemplo, 20x20 pixels)
        self.icon = self.icon.resize((20, 20), Image.LANCZOS)
        self.icon = ImageTk.PhotoImage(self.icon)
        
        self.iconmongo = Image.open('mongodb.png')
        # Redimensionar a imagem para um tamanho adequado (por exemplo, 20x20 pixels)
        self.iconmongo = self.iconmongo.resize((20, 20), Image.LANCZOS)
        self.iconmongo = ImageTk.PhotoImage(self.iconmongo)
        
        bg_color = self.tab1view2._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.tab1view2._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self.tab1view2._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0, font=("Arial Black", 14), padding=5, spacing=20)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        self.tab1view2.bind("<<TreeviewSelect>>", lambda event: self.tab1view2.focus_set())

        
        ##Treeview widget data
        self.treeview = ttk.Treeview(self.listbox_tables, height=10, show="tree")
        self.treeview.insert('', '0', 'i1', text ='MySQL', image=self.icon)
        self.treeview.bind("<ButtonRelease-1>", self.show_table_data)
        self.treeview.grid(padx=10)

        self.treeviewMongo = ttk.Treeview(self.listbox_tables_mongo, height=10, show="tree")
        self.treeviewMongo.insert('', '0', 'i1', text ='MongoDB', image=self.iconmongo)
        self.treeviewMongo.bind("<ButtonRelease-1>", self.show_collection_data)
        self.treeviewMongo.grid(padx=10)
        
        
        self.switch = ctk.CTkSwitch(self.tab,
                                    text=None,
                                    variable=self.switch_state,
                                    command=self.change_color,
                                    onvalue=True,
                                    offvalue=False)
        self.switch.pack(side="top", padx=1, pady=1, anchor="w")
            
        self.text_switch = ctk.CTkLabel(self.tab, text="")
        self.text_switch.pack(side="top", padx=1, pady=1, anchor="w")
        
        self.terminal = ctk.CTkTextbox(self.tab, wrap="word")
        self.terminal.pack(fill="both", expand=True)
    
        
        self.migrate_mysql_to_mongo_button = ctk.CTkButton(self.tab, text="Iniciar", command=self.mudarcor)
        self.migrate_mysql_to_mongo_button.pack(side="right", padx=10, pady=10)
        
        
        self.btlimpar = ctk.CTkButton(master=self.tab, text="Limpar", command=self.limpar)
        self.btlimpar.pack(side="left", padx=10, pady=10)
        
        self.progress = ctk.CTkProgressBar(master=self.tab,width=200,height=20,border_width=5)
        self.progress.pack(side="bottom", padx=10, pady=10)
        
        
        self.progress.set(0)
        
        self.change_color() 
        
        self.menubar()  
        
        self.root.mainloop()
        

    def mudarcor(self):
        if self.background == "mysql":
            self.compile_and_migrate_data()
        else:
            self.migrate_mongo_to_mysql()
            
    
    def change_color(self):
        print("Switch state:", self.switch_state.get())  # Debugging
        if self.switch_state.get():  # Se o switch estiver ativado
            self.background = "mysql"
            self.switch.configure(fg_color="blue")
            self.migrate_mysql_to_mongo_button.configure(fg_color="blue", hover_color="gray")
            self.tabview.configure(segmented_button_selected_color="blue", segmented_button_selected_hover_color="gray")
            self.tabviewschema.configure(segmented_button_selected_color="blue", segmented_button_selected_hover_color="gray") 
            self.listbox_tables.configure(highlight_color="blue", border_color="blue")
            self.terminal.configure(border_color="blue")
            self.listbox_tables_mongo.configure(border_color="blue")
            self.btlimpar.configure(fg_color="blue", hover_color="gray")
            self.progress.configure(border_color = "blue", fg_color="gray", progress_color="blue")
            self.text_switch.configure(text="MySQL para MongoDB", text_color="blue")
        else:
            self.background = "mongodb"  # Debugging
            self.migrate_mysql_to_mongo_button.configure(fg_color="green", hover_color="gray")
            self.switch.configure(fg_color="green")
            self.btlimpar.configure(fg_color="green", hover_color="gray")
            self.terminal.configure(border_color="green")
            self.progress.configure(border_color = "green", fg_color="gray", progress_color="green")
            self.tabview.configure(segmented_button_selected_color="green", segmented_button_selected_hover_color="gray")
            self.tabviewschema.configure(segmented_button_selected_color="green", segmented_button_selected_hover_color="gray") 
            self.listbox_tables_mongo.configure(highlight_color="green", hover_color="green", border_color="green")
            self.listbox_tables.configure(border_color="green")
            self.text_switch.configure(text="MongoDB para MySQL", text_color="green")
        self.tab.update()
      
                
    def list_mysql_tables(self):
            if hasattr(self, 'mysql_connection'):
                try:
                    cursor = self.mysql_connection.cursor()
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    for idx, table in enumerate(tables, start=1):
                        self.treeview.insert('i1', 'end', f'table_{idx}', text=table[0])
                    cursor.close()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Please connect to MySQL first.")
            
            
    def list_mongo_collections(self):
        if hasattr(self, 'mongo_client'):
            try:
                database_name = self.database_mongo.get()
                db = self.mongo_client[database_name]
                collections = db.list_collection_names()
                for collection in collections:
                    self.treeviewMongo.insert('i1', 'end', text=collection)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please connect to MongoDB first.")

    def show_table_data(self, event):
        item = self.treeview.selection()[0]  # Pegar o item selecionado na treeview
        table_name = self.treeview.item(item, "text")  # Pegar o nome da tabela selecionada
        if hasattr(self, 'mysql_connection'):
            try:
                cursor = self.mysql_connection.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")  # Selecionar todos os dados da tabela
                table_data = cursor.fetchall()  # Trazer todos os dados da tabela
                self.terminal.delete('1.0', 'end')  # Limpar o terminal antes de mostrar os novos dados
                
                # Formatar os dados da tabela no terminal
                self.terminal.insert('end', '{\n')
                for row in table_data:
                    formatted_row = '\t\t\t'.join(str(value) for value in row)  # Formatar cada linha com os valores separados por tabulação
                    self.terminal.insert('end', f"\t{formatted_row}\n")  # Adicionar a linha formatada no terminal
                self.terminal.insert('end', '}\n')

                cursor.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please connect to MySQL first.")
            
    def show_collection_data(self, _=None):  # Adicione um argumento padrão para o evento Tkinter
        item = self.treeviewMongo.selection()[0]  # Pegar o item selecionado na treeview
        collection_name = self.treeviewMongo.item(item, "text")  # Pegar o nome da coleção selecionada
        if hasattr(self, 'mongo_client'):
            try:
                database_name = self.database_mongo.get()
                db = self.mongo_client[database_name]
                collection_data = db[collection_name].find()  # Buscar os documentos da coleção
                self.terminal.delete('1.0', 'end')  # Limpar o terminal antes de mostrar os novos dados
                for document in collection_data:
                    formatted_document = "{" + ''.join(f'\n    "{key}": {value},' for key, value in document.items()) + "\n}"
                    self.terminal.insert('end', f"{formatted_document}\n") 
                    # Mostrar os documentos da coleção no terminal
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please connect to MongoDB first.")
            
    def menubar(self): 
        self.label_localhost = ctk.CTkLabel(self.tab1, text="Localhost:")
        self.label_localhost.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
        self.localhost = ctk.CTkEntry(self.tab1, placeholder_text="Localhost")
        self.localhost.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        
        self.label_porta = ctk.CTkLabel(self.tab1, text="Porta:")
        self.label_porta.place(relx=0.35, rely=0.3, anchor=tk.CENTER)
        self.porta = ctk.CTkEntry(self.tab1, placeholder_text="Porta")
        self.porta.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        
        self.label_usuario = ctk.CTkLabel(self.tab1, text="Usuario:")
        self.label_usuario.place(relx=0.35, rely=0.4, anchor=tk.CENTER)
        self.usuario = ctk.CTkEntry(self.tab1, placeholder_text="Usuario")
        self.usuario.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        self.label_senha = ctk.CTkLabel(self.tab1, text="Senha:")
        self.label_senha.place(relx=0.35, rely=0.5, anchor=tk.CENTER)
        self.senha = ctk.CTkEntry(self.tab1, placeholder_text="Senha", show="*")
        self.senha.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.label_database = ctk.CTkLabel(self.tab1, text="Database:")
        self.label_database.place(relx=0.35, rely=0.6, anchor=tk.CENTER)
        self.database = ctk.CTkEntry(self.tab1, placeholder_text="Database")
        self.database.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        self.conect = ctk.CTkButton(self.tab1, text="Conectar", fg_color="blue", command=self.conectar_mysql)
        self.conect.pack(side="bottom", padx=10, pady=10)

        self.label_localhost_mongo = ctk.CTkLabel(self.tab2, text="Localhost:")
        self.label_localhost_mongo.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
        self.localhost_mongo = ctk.CTkEntry(self.tab2, placeholder_text="Localhost")
        self.localhost_mongo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        self.label_porta_mongo = ctk.CTkLabel(self.tab2, text="Porta:")
        self.label_porta_mongo.place(relx=0.35, rely=0.3, anchor=tk.CENTER)
        self.porta_mongo = ctk.CTkEntry(self.tab2, placeholder_text="Porta")
        self.porta_mongo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        self.label_usuario_mongo = ctk.CTkLabel(self.tab2, text="Usuario:")
        self.label_usuario_mongo.place(relx=0.35, rely=0.4, anchor=tk.CENTER)
        self.usuario_mongo = ctk.CTkEntry(self.tab2, placeholder_text="Usuario")
        self.usuario_mongo.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        self.label_senha_mongo = ctk.CTkLabel(self.tab2, text="Senha:")
        self.label_senha_mongo.place(relx=0.35, rely=0.5, anchor=tk.CENTER)
        self.senha_mongo = ctk.CTkEntry(self.tab2, placeholder_text="Senha")
        self.senha_mongo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.label_database_mongo = ctk.CTkLabel(self.tab2, text="Database:")
        self.label_database_mongo.place(relx=0.35, rely=0.6, anchor=tk.CENTER)
        self.database_mongo = ctk.CTkEntry(self.tab2, placeholder_text="Database")
        self.database_mongo.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.conect_mongo = ctk.CTkButton(self.tab2, text="Conectar", fg_color="green",hover_color="gray", command=self.conectar_mongodb)
        self.conect_mongo.pack(side="bottom", padx=10, pady=10)

        self.tabview.pack()  
        
   
    def limpar(self):
        self.terminal.delete("1.0",ctk.END)
        self.progress.set(0)
    
    def conectar_mysql(self):
        mysql_host = self.localhost.get()
        mysql_port = self.porta.get()
        mysql_user = self.usuario.get()
        mysql_password = self.senha.get()
        mysql_database = self.database.get()
        
        try:
            self.mysql_connection = pymysql.connect(
                host=mysql_host,
                port=int(mysql_port),
                user=mysql_user,
                password=mysql_password,
                database=mysql_database
            )
            messagebox.showinfo("Info", "Conectado ao MySQL com sucesso!!")
            self.list_mysql_tables()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def conectar_mongodb(self):
        mongo_host = self.localhost_mongo.get()
        mongo_port = int(self.porta_mongo.get())
        mongo_usuario = self.usuario_mongo.get()
        mongo_senha = self.senha_mongo.get()
        mongo_database = self.database_mongo.get()


        try:
            if mongo_host and mongo_port:
                self.mongo_client = MongoClient(mongo_host, mongo_port)
            elif mongo_usuario and mongo_senha and mongo_database:
                self.mongo_client = MongoClient(mongo_host, mongo_port, mongo_usuario, mongo_senha, mongo_database)
            elif mongo_usuario:
                self.mongo_client = MongoClient(mongo_host, mongo_port, mongo_usuario)        
            elif mongo_senha:
                self.mongo_client = MongoClient(mongo_host, mongo_port, mongo_senha)
            elif mongo_database:
                self.mongo_client = MongoClient(mongo_host, mongo_port, mongo_database)  

            messagebox.showinfo("Info", "Conectado ao MongoDB com sucesso!!")
            self.list_mongo_collections()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    #MIGRAÇÃO MYSQL PARA MONGODB
    def compile_and_migrate_data(self):
        try:
            if hasattr(self, 'mysql_connection') and hasattr(self, 'mongo_client'):
                self.migrate_mysql_to_mongodb()
            else:
                messagebox.showerror("Erro", "Por favor conecte ao MySQL e MongoDB.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
            
    def migrate_mysql_to_mongodb(self):
        mysql_db = self.database.get()
        self.mongo_db = self.mongo_client[mysql_db]
        cursor = self.mysql_connection.cursor()
        cursor.execute("DROP TABLE IF EXIST '{mysql_db}'")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        total_tables = len(tables)
        current_table = 0
        
        for table in tables:
            table_name = table[0]
            self.migrate_data_from_mysql_to_mongodb(table_name, self.mongo_db[table_name])
            current_table +=1
            progress_percent = (current_table / total_tables) * 100
            self.progress.set(progress_percent)
            self.progress.update()
            self.root.update_idletasks()
        
        self.terminal.insert("end", "Migração feita com sucesso!!.\n")
        self.list_mongo_collections()
        messagebox.showinfo("","Migração feita com sucesso!!")

    
    def migrate_data_from_mysql_to_mongodb(self, mysql_table, mongo_collection):
        cursor = self.mysql_connection.cursor()
        cursor.execute(f"SELECT * FROM {mysql_table}")
        data = cursor.fetchall()
        
        for row in data:
            row_list = [self.decimal_to_string(value) for value in row]
            row_list = [self.date_to_datetime(value) for value in row_list]
            documento = dict(zip([column[0] for column in cursor.description], row_list))
            
            try:
                self.result = mongo_collection.insert_one(documento)
                self.terminal.insert("end", f"Inserted document into MongoDB: {documento}\n")
            except Exception as e:
                self.terminal.insert("end", f"Error inserting document into MongoDB: {e}\n")
                
    def decimal_to_string(self, value):
        if isinstance(value, Decimal):
            return str(value)
        return value
    
    def date_to_datetime(self, value):
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        return value

    #MIGRAÇÃO MONGO PARA MYSQL
    def migrate_mongo_to_mysql(self):
        try:
            if hasattr(self, 'mysql_connection') and hasattr(self, 'mongo_client'):
                self.create_mysql_tables_from_mongodb_schema()
                self.migrate_data_from_mongodb_to_mysql()
            else:
                messagebox.showerror("Erro", "Por favor conecte ao MySQL e MongoDB.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def create_mysql_tables_from_mongodb_schema(self):
        mongo_db_name = self.database_mongo.get()
        mongo_db = self.mongo_client[mongo_db_name]

        cursor = self.mysql_connection.cursor()

        for collection_name in mongo_db.list_collection_names():
            collection = mongo_db[collection_name]
            sample_document = collection.find_one()

            # Verifica se a tabela já existe
            cursor.execute(f"SHOW TABLES LIKE '{collection_name}'")
            existing_tables = cursor.fetchall()
            
            if sample_document: 
                if not existing_tables:
                    # Remove a coluna _id
                    sample_document.pop('_id', None)

                    # Analisa os tipos de dados das colunas
                    columns = {}
                    for key, value in sample_document.items():
                        if isinstance(value, int):
                            columns[key] = "INT"
                        elif isinstance(value, float):
                            columns[key] = "FLOAT"
                        elif isinstance(value, str):
                            columns[key] = "VARCHAR(255)"
                        elif isinstance(value, bool):
                            columns[key] = "BOOLEAN"
                        elif isinstance(value, datetime.datetime):
                            columns[key] = "DATETIME"
                        # Adicione mais tipos de dados conforme necessário

                    # Adiciona o campo id e define como PRIMARY KEY se o nome da tabela for igual ao nome da coluna
                    if '_id' in sample_document:
                        columns['_id'] = "INT PRIMARY KEY AUTO_INCREMENT"

                    # Criação da tabela no MySQL se ela não existir
                    columns_sql = ", ".join([f"{column} {datatype}" for column, datatype in columns.items()])
                    sql = f"CREATE TABLE {collection_name} ({columns_sql})"
                    cursor.execute(sql)
                    print(f"Created MySQL table '{collection_name}'")

        cursor.close()

                
    def migrate_data_from_mongodb_to_mysql(self):
        try:
            if hasattr(self, 'mysql_connection') and hasattr(self, 'mongo_client'):
                mysql_db_name = self.database_mongo.get()
                mongo_db = self.mongo_client[mysql_db_name]

                cursor = self.mysql_connection.cursor()
                total_collections = len(mongo_db.list_collection_names())
                current_collection = 0

                for collection_name in mongo_db.list_collection_names():
                    collection = mongo_db[collection_name]

                    for document in collection.find():
                        document.pop('_id', None)
                        values = []
                        for value in document.values():
                            if isinstance(value, str):
                                values.append(f"'{value}'")
                            elif isinstance(value, datetime.datetime):
                                values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
                            else:
                                values.append(str(value))

                        columns = ", ".join(document.keys())
                        values_str = ", ".join(values)

                        sql = f"INSERT INTO {collection_name} ({columns}) VALUES ({values_str})"
                        cursor.execute(sql)
                        self.terminal.insert("end",f"Inserted document into MySQL table '{collection_name}'")

                    current_collection += 1
                    progress_percent = (current_collection / total_collections) * 100
                    self.progress.set(progress_percent)
                    self.progress.update()
                    self.root.update_idletasks()
                    
                self.mysql_connection.commit()
                self.terminal.insert("end","Data migration from MongoDB to MySQL completed.")
                messagebox.showinfo("","Migração feita com sucesso!!")
                self.list_mysql_tables()
            else:
                messagebox.showerror("Error", "Please connect to MySQL and MongoDB.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def fechar_conexoes(self):
        self.mysql_connection.close()
        self.mongo_client.close()
        
if __name__ == "__main__":
    app = MigrationApp()
