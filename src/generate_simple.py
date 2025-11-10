import pandas as pd

# Lê o arquivo CSV
csv_path = 'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv'
df = pd.read_csv(csv_path, sep=';', encoding='latin1')

# Cria o HTML básico
html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sistema de Busca</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        input { width: 100%; padding: 8px; margin: 4px 0; }
        .search { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="search">
        <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Digite para pesquisar...">
    </div>
    <table id="dataTable">
        <thead>
            <tr>
                <th>Endereço</th>
                <th>Bairro</th>
                <th>CEP</th>
                <th>NAP</th>
                <th>Contrato</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
'''

# Adiciona as linhas da tabela
for _, row in df.iterrows():
    html += f'''
            <tr>
                <td>{row['DSC_ENDERECO_COMPLETO']}</td>
                <td>{row['DSC_BAIRRO']}</td>
                <td>{row['NUM_CEP']}</td>
                <td>{row['NAP']}</td>
                <td>{row['NUM_CONTRATO']}</td>
                <td>{row['STATUS']}</td>
            </tr>'''

# Adiciona o JavaScript e fecha o HTML
html += '''
        </tbody>
    </table>
    <script>
    function filterTable() {
        var input = document.getElementById("searchInput");
        var filter = input.value.toLowerCase();
        var rows = document.getElementById("dataTable").getElementsByTagName("tr");

        for (var i = 1; i < rows.length; i++) {
            var show = false;
            var cells = rows[i].getElementsByTagName("td");
            
            for (var j = 0; j < cells.length; j++) {
                var cell = cells[j];
                if (cell) {
                    var text = cell.textContent || cell.innerText;
                    if (text.toLowerCase().indexOf(filter) > -1) {
                        show = true;
                        break;
                    }
                }
            }
            
            rows[i].style.display = show ? "" : "none";
        }
    }
    </script>
</body>
</html>
'''

# Salva o arquivo HTML
with open('src/templates/sistema.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Arquivo HTML gerado com sucesso!")