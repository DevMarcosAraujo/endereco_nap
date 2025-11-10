import pandas as pd

print("Carregando dados...")
df = pd.read_csv(
    'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv',
    sep=';',
    encoding='latin1'
)

# Pega um exemplo de NAP para verificar
print("Exemplo de NAP:")
print(df['COD_NODE'].head())