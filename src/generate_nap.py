import pandas as pd

print("Carregando dados...")
df = pd.read_csv(
    'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv',
    sep=';',
    encoding='latin1',
    usecols=['COD_NODE', 'DSC_ENDERECO_COMPLETO', 'DSC_STATUS_CONTRATO', 'NUM_CONTRATO', 'STATUS'],
    dtype=str  # Força todas as colunas como texto
)

html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Busca de NAP</title>
    <style>
        body { 
            font-family: Arial; 
            margin: 20px; 
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .search-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        .search-input {
            width: 300px;
            padding: 12px;
            font-size: 18px;
            border: 2px solid #1a73e8;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .search-info {
            color: #666;
            margin-top: 10px;
        }
        table { 
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td { 
            padding: 12px; 
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #1a73e8;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .highlight {
            background-color: #ffd700;
            font-weight: bold;
        }
        #resultInfo {
            margin: 10px 0;
            padding: 10px;
            background-color: #e8f0fe;
            border-radius: 4px;
            color: #1a73e8;
            font-weight: bold;
        }
        .table-container {
            max-height: 600px;
            overflow-y: auto;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-box">
            <input type="text" id="searchInput" class="search-input" placeholder="Digite o número do NAP (ex: CTO0010505)" autofocus>
            <div class="search-info">Digite o número do NAP para ver os resultados</div>
            <div id="resultInfo"></div>
        </div>
        
        <div class="table-container">
            <table id="dataTable">
                <thead>
                    <tr>
                        <th>NAP</th>
                        <th>Endereço</th>
                        <th>Status</th>
                        <th>Contrato</th>
                        <th>Situação</th>
                    </tr>
                </thead>
                <tbody>
'''

# Adiciona as linhas da tabela
for _, row in df.iterrows():
    html += f'''
                <tr data-nap="{row['COD_NODE'].lower()}">
                    <td>{row['COD_NODE']}</td>
                    <td>{row['DSC_ENDERECO_COMPLETO']}</td>
                    <td>{row['DSC_STATUS_CONTRATO']}</td>
                    <td>{row['NUM_CONTRATO']}</td>
                    <td>{row['STATUS']}</td>
                </tr>'''

html += '''
                </tbody>
            </table>
        </div>
    </div>

    <script>
    document.getElementById('searchInput').addEventListener('input', function() {
        var input = this.value.toLowerCase();
        var rows = document.getElementById('dataTable').getElementsByTagName('tr');
        var count = 0;
        var MAX_RESULTS = 100;
        
        // Remove highlights anteriores
        document.querySelectorAll('.highlight').forEach(function(el) {
            el.classList.remove('highlight');
        });
        
        // Começa do índice 1 para pular o cabeçalho
        for (var i = 1; i < rows.length && count < MAX_RESULTS; i++) {
            var row = rows[i];
            var nap = row.getAttribute('data-nap');
            var shouldShow = nap.includes(input);
            
            if (shouldShow) {
                row.style.display = '';
                if (input) {
                    row.cells[0].classList.add('highlight');
                }
                count++;
            } else {
                row.style.display = 'none';
            }
        }
        
        // Atualiza informações de resultado
        var info = '';
        if (input) {
            info = count + ' NAP(s) encontrado(s)';
            if (count >= MAX_RESULTS) {
                info += ' (mostrando primeiros ' + MAX_RESULTS + ' resultados)';
            }
        } else {
            info = 'Digite um NAP para pesquisar';
        }
        document.getElementById('resultInfo').textContent = info;
    });

    // Dispara a busca inicial
    document.getElementById('searchInput').dispatchEvent(new Event('input'));
    </script>
</body>
</html>
'''

# Salva o arquivo HTML
with open('src/templates/sistema.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Arquivo HTML gerado com sucesso!")