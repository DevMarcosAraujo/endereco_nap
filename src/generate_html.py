import pandas as pd
import os

# Lê o arquivo CSV
csv_path = 'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv'
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

# Cria o HTML
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sistema de Busca</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f2f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a73e8;
            text-align: center;
            margin-bottom: 30px;
        }
        .search-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .input-group {
            flex: 1;
            min-width: 200px;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            color: #333;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .search-button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .search-button:hover {
            background-color: #1557b0;
        }
        .results {
            margin-top: 30px;
            overflow-x: auto;
        }
    </style>
    <script>
        function filterTable() {
            const endereco = document.getElementById('endereco').value.toLowerCase();
            const bairro = document.getElementById('bairro').value.toLowerCase();
            const cep = document.getElementById('cep').value.toLowerCase();
            const nap = document.getElementById('nap').value.toLowerCase();
            const contrato = document.getElementById('contrato').value.toLowerCase();
            
            const rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const cells = row.getElementsByTagName('td');
                const shouldShow = (
                    cells[0].textContent.toLowerCase().includes(endereco) &&
                    cells[1].textContent.toLowerCase().includes(bairro) &&
                    cells[2].textContent.toLowerCase().includes(cep) &&
                    cells[3].textContent.toLowerCase().includes(nap) &&
                    cells[4].textContent.toLowerCase().includes(contrato)
                );
                row.style.display = shouldShow ? '' : 'none';
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Sistema de Busca</h1>
        
        <div class="search-container">
            <div class="input-group">
                <label for="endereco">Endereço:</label>
                <input type="text" id="endereco" onkeyup="filterTable()" placeholder="Digite o endereço...">
            </div>
            <div class="input-group">
                <label for="bairro">Bairro:</label>
                <input type="text" id="bairro" onkeyup="filterTable()" placeholder="Digite o bairro...">
            </div>
            <div class="input-group">
                <label for="cep">CEP:</label>
                <input type="text" id="cep" onkeyup="filterTable()" placeholder="Digite o CEP...">
            </div>
            <div class="input-group">
                <label for="nap">NAP:</label>
                <input type="text" id="nap" onkeyup="filterTable()" placeholder="Digite o NAP...">
            </div>
            <div class="input-group">
                <label for="contrato">Contrato:</label>
                <input type="text" id="contrato" onkeyup="filterTable()" placeholder="Digite o contrato...">
            </div>
        </div>

        <div class="results">
            <table>
                <thead>
                    <tr>
                        <th>Endereço</th>
                        <th>Bairro</th>
                        <th>CEP</th>
                        <th>NAP</th>
                        <th>Contrato</th>
                        <th>Status</th>
                        <th>Situação Comercial</th>
                    </tr>
                </thead>
                <tbody>


# Adiciona as linhas da tabela
for _, row in df.head(1000).iterrows():  # Limitando a 1000 registros para performance
    html_content += f"""
                    <tr>
                        <td>{row['DSC_ENDERECO_COMPLETO']}</td>
                        <td>{row['DSC_BAIRRO']}</td>
                        <td>{row['NUM_CEP']}</td>
                        <td>{row['NAP']}</td>
                        <td>{row['NUM_CONTRATO']}</td>
                        <td>{row['STATUS']}</td>
                        <td>{row['DSC_SITUACAO_COMERCIAL']}</td>
                    </tr>
    

html_content += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>

# Salva o arquivo HTML
with open('src/templates/sistema.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Arquivo HTML gerado com sucesso!")