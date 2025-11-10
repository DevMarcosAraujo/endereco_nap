                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    import pandas as pd
import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Inicializa o banco de dados a partir do arquivo CSV"""
        if not Path(self.db_path).exists():
            # Carrega o arquivo CSV da pasta templates/planilha
            csv_path = Path('src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv')
            df = pd.read_csv(csv_path)
            
            # Conecta ao SQLite e salva o DataFrame
            conn = sqlite3.connect(self.db_path)
            df.to_sql('dados', conn, if_exists='replace', index=False)
            conn.close()

    def search(self, query):
        """
        Realiza busca no banco de dados
        query: dicionário com os parâmetros de busca
        """
        conn = sqlite3.connect(self.db_path)
        
        # Constrói a query SQL baseada nos parâmetros
        sql = """
            SELECT 
                DSC_ENDERECO_COMPLETO, DSC_BAIRRO, NUM_CEP, 
                NAP, NUM_CONTRATO, STATUS, DSC_SITUACAO_COMERCIAL,
                DSC_SITUACAO_TECNICA_PTV, DSC_SITUACAO_TEC_VIRTUA
            FROM dados 
            WHERE 1=1
        """
        params = []
        
        for column, value in query.items():
            if value:
                sql += f" AND {column} LIKE ?"
                params.append(f"%{value}%")
        
        # Executa a busca
        df = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        
        # Limita a 100 resultados para melhor performance
        df = df.head(100)
        return df.to_dict('records')