import pandas as pd
import os

# Lê o arquivo CSV
import pandas as pd
import os
import json

# Lê o arquivo CSV
csv_path = 'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv'
df = pd.read_csv(csv_path, sep=';', encoding='latin1')

# Calcula estatísticas
total_naps = len(df['NAP'].unique())
total_conectados = len(df[df['STATUS'] == 'CONECTADO'])
total_desconectados = len(df[df['STATUS'].str.contains('DESCONECTADO', na=False)])
total_enderecos = len(df)

# Calcula percentuais para o gráfico
status_counts = df['STATUS'].value_counts()
total = status_counts.sum()
status_percentages = (status_counts / total * 100).round(1)

# Monta um dicionário agrupado por NAP para carregar sob demanda (muito mais leve que HTML completo)
data_by_nap = {}
for _, row in df.iterrows():
    nap = str(row['NAP']) if not pd.isna(row['NAP']) else ''
    if not nap:
        continue
    key = nap.lower()
    record = {
        'NAP': nap,
        'DSC_ENDERECO_COMPLETO': str(row.get('DSC_ENDERECO_COMPLETO', '')),
        'COD_NODE': str(row.get('COD_NODE', '')),
        'DSC_STATUS_CONTRATO': str(row.get('DSC_STATUS_CONTRATO', '')),
        'NUM_CONTRATO': str(row.get('NUM_CONTRATO', '')),
        'SITUACAO': str(row.get('DSC_SITUACAO_COMERCIAL', ''))
    }
    data_by_nap.setdefault(key, []).append(record)

# Salva JSON agrupado por NAP
os.makedirs('src/templates', exist_ok=True)
with open('src/templates/data_by_nap.json', 'w', encoding='utf-8') as jf:
    json.dump(data_by_nap, jf, ensure_ascii=False)

print("JSON gerado com sucesso: src/templates/data_by_nap.json")