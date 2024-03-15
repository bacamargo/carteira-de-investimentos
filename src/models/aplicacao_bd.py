import psycopg2
import sql.tables as tables
import json

class Bd_postgres:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def create_connection(self, path_json='./src/models/credentials/credentials.json'):

        with open(path_json, 'r') as file:
            data = json.load(file)

        self.connection = psycopg2.connect(
            dbname=data['NAME_BD'], user=data['USERNAME'], password=data['PASSWORD'], host=data['HOST'], port=data['PORT']
        )
        self.cursor = self.connection.cursor()

    
    def disconnect(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()
    
    def create_tables(self):
        self.cursor.execute(tables.operations_table)
        self.cursor.execute(tables.client_table)
        self.cursor.execute(tables.wallets_table)

        self.connection.commit()
    
    def columns_table(self, table_postgres):
        try:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ORDINAL_POSITION"
            self.cursor.execute(query, (table_postgres,))
            columns = [row[0] for row in self.cursor.fetchall()]
            return columns
        
        except psycopg2.Error as e:
            print(e)
            return None

    
    def inserir(self, table_postgres, values):
        try:
            columns = self.columns_table(table_postgres)[1:]
            query = f"INSERT INTO {table_postgres} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))}) "
            self.cursor.execute(query, values)
            self.connection.commit()

        except psycopg2.Error as e:
            print(e)

    
    def search_nome(self, table_postgres, nome):
        try:
            query = f"SELECT * FROM {table_postgres} WHERE nome = %s"
            self.cursor.execute(query, (nome,))
            data = self.cursor.fetchone()
            if data:
                for row in data:
                    print(row)
            else:
                print(None)

        except psycopg2.Error as e:
            print(e)

    
    def delete(self, table_postgres, column_name, column_value):
        try:
            query = f"DELETE FROM {table_postgres} WHERE {column_name} = %s"
            self.cursor.execute(query, (column_value,))
            self.connection.commit()
            print("Registro removido com sucesso!")

        except psycopg2.Error as e:
            print(e)

    
    def select(self, table_postgres):
        try:
            query = f"SELECT * FROM {table_postgres}"
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            if data:
                for d in data:
                    print(d)
            else:
                print("Nenhum registro encontrado.")

        except psycopg2.Error as e:
            print(e)

    
    def select_where(self, table_postgres, column_name, column_value):
        try:
            query = f"SELECT * FROM {table_postgres} WHERE {column_name} = %s"
            self.cursor.execute(query, (column_value,))
            data = self.cursor.fetchall()
            if data:
                for row in data:
                    print(row) 
            else:
                print(None)
                
        except psycopg2.Error as e:
            print(e)
            
    
    def update(self, tabela, id_registro, valores):
        try:
            columns = self.columns_table(tabela)
            set_clause = ", ".join([f"{column} = %s" for column in columns])
            query = f"UPDATE {tabela} SET {set_clause} WHERE id_cliente = %s"
            self.cursor.execute(query, valores + (id_registro,))
            self.connection.commit()
            print("Registro alterado com sucesso!")

        except psycopg2.Error as e:
            print(e)
            
    def search_client_id(self, values):
        try:
            query = f"SELECT id_cliente FROM clients WHERE cpf = %s AND senha = %s"
            self.cursor.execute(query, values)
            data = self.cursor.fetchone()
            if data:
                return data[0]
            else:
                return -1

        except psycopg2.Error as e:
            print(e)
