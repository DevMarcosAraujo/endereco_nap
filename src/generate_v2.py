import pandas as pd
import plotly.express as px
import json

# Lê o arquivo CSV com apenas as colunas necessárias
colunas = [
    'DSC_ENDERECO_COMPLETO',
    'DSC_STATUS_CONTRATO',
    'NUM_CONTRATO',
    'COD_NODE',
    'STATUS',
    'DSC_SITUACAO_COMERCIAL'
]

# Lê o CSV otimizado
print("Carregando dados...")
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import base64

# Lê o arquivo CSV
csv_path = 'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv'
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

# Calcula estatísticas
total_naps = len(df['NAP'].unique())
total_conectados = len(df[df['STATUS'] == 'CONECTADO'])
total_desconectados = len(df[df['STATUS'].str.contains('DESCONECTADO', na=False)])
total_enderecos = len(df)

# Cria gráfico de status
status_counts = df['STATUS'].value_counts()
fig_status = go.Figure(data=[
    go.Pie(labels=status_counts.index, 
           values=status_counts.values,
           hole=.3,
           marker_colors=['#DA291C', '#666666', '#999999'])
])
fig_status.update_layout(
    title='Distribuição de Status',
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True
)
chart_status = fig_status.to_html(full_html=False)

# Gráfico de barras para NAPs mais utilizados
top_naps = df['NAP'].value_counts().head(10)
fig_naps = go.Figure(data=[
    go.Bar(x=top_naps.index, 
           y=top_naps.values,
           marker_color='#DA291C')
])
fig_naps.update_layout(
    title='Top 10 NAPs mais utilizados',
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis_title='NAP',
    yaxis_title='Quantidade de Endereços'
)
chart_naps = fig_naps.to_html(full_html=False)

# Calcula estatísticas
print("Calculando estatísticas...")
status_counts = df['DSC_STATUS_CONTRATO'].value_counts().head(10)
status_data = [{'status': k, 'quantidade': int(v)} for k, v in status_counts.items()]

# Cria o gráfico com Plotly
fig = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title='Distribuição por Status'
)
grafico_json = fig.to_json()

# Cria o HTML
print("Gerando HTML...")
html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sistema de Busca</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ 
            font-family: Arial; 
            margin: 20px; 
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .card h3 {{
            margin: 0;
            color: #666;
        }}
        .card .number {{
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
            color: #1a73e8;
        }}
        .search-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        table {{ 
            border-collapse: collapse; 
            width: 100%;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 12px; 
            text-align: left; 
        }}
        th {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        input {{ 
            width: 100%; 
            padding: 8px;
            margin: 4px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .status-ativo {{ color: #28a745; }}
        .status-desconectado {{ color: #dc3545; }}
        .status-cancelado {{ color: #6c757d; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="dashboard">
            <div class="card">
                <h3>Total de Registros</h3>
                <div class="number">{len(df):,}</div>
            </div>
            <div class="card">
                <h3>Ativos</h3>
                <div class="number">{len(df[df['DSC_STATUS_CONTRATO'].str.contains('ATIVO', na=False, case=False)]):,}</div>
            </div>
            <div class="card">
                <h3>Desconectados</h3>
                <div class="number">{len(df[df['DSC_STATUS_CONTRATO'].str.contains('DESCONECTADO', na=False, case=False)]):,}</div>
            </div>
        </div>

        <div class="chart-container">
            <div id="chart"></div>
        </div>

        <div class="search-container">
            <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Digite para pesquisar...">
        </div>

        <table id="dataTable">
            <thead>
                <tr>
                    <th>Endereço</th>
                    <th>Status</th>
                    <th>Contrato</th>
                    <th>NAP</th>
                    <th>Situação</th>
                </tr>
            </thead>
            <tbody>
'''

# Adiciona as linhas da tabela (limitando a 1000 registros inicialmente para performance)
for _, row in df.head(1000).iterrows():
    status_class = ''
    if 'ATIVO' in str(row['DSC_STATUS_CONTRATO']).upper():
        status_class = 'status-ativo'
    elif 'DESCONECTADO' in str(row['DSC_STATUS_CONTRATO']).upper():
        status_class = 'status-desconectado'
    elif 'CANCELADO' in str(row['DSC_STATUS_CONTRATO']).upper():
        status_class = 'status-cancelado'

    html += f'''
            <tr>
                <td>{row['DSC_ENDERECO_COMPLETO']}</td>
                <td class="{status_class}">{row['DSC_STATUS_CONTRATO']}</td>
                <td>{row['NUM_CONTRATO']}</td>
                <td>{row['COD_NODE']}</td>
                <td>{row['STATUS']}</td>
            </tr>'''

# Adiciona o JavaScript e fecha o HTML
html += f'''
        </tbody>
    </table>

    <script>
    // Carrega o gráfico
    var graphData = {grafico_json};
    Plotly.newPlot('chart', graphData.data, graphData.layout);

    function filterTable() {{
        var input = document.getElementById("searchInput");
        var filter = input.value.toLowerCase();
        var rows = document.getElementById("dataTable").getElementsByTagName("tr");
        var count = 0;
        const MAX_VISIBLE = 100; // Limita a 100 resultados para performance

        for (var i = 1; i < rows.length && count < MAX_VISIBLE; i++) {{
            var show = false;
            var cells = rows[i].getElementsByTagName("td");
            
            for (var j = 0; j < cells.length; j++) {{
                var cell = cells[j];
                if (cell) {{
                    var text = cell.textContent || cell.innerText;
                    if (text.toLowerCase().indexOf(filter) > -1) {{
                        show = true;
                        break;
                    }}
                }}
            }}
            
            if (show) {{
                rows[i].style.display = "";
                count++;
            }} else {{
                rows[i].style.display = "none";
            }}
        }}
    }}
    </script>
</body>
</html>
'''

# Salva o arquivo HTML
with open('src/templates/sistema.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Arquivo HTML gerado com sucesso!")