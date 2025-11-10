# Sistema de Busca NAP

Sistema web para visualização e busca de informações de NAPs (Network Access Points).

## Funcionalidades

- Busca por NAP ou endereço
- Visualização de status de contrato
- Exibição de endereços completos
- Interface otimizada para grandes volumes de dados

## Como usar

1. Coloque o arquivo CSV na pasta `src/templates/planilha/`
2. Execute o script de geração de dados:
   ```bash
   python3 src/generate_v3.py
   ```
3. Inicie o servidor HTTP:
   ```bash
   python3 -m http.server 8000
   ```
4. Acesse no navegador: `http://localhost:8000/src/templates/sistema.html`

## Estrutura do Projeto

- `src/`: Código fonte do projeto
  - `generate_v3.py`: Script para gerar JSON dos dados
  - `templates/`: Arquivos da interface web
    - `sistema.html`: Interface principal
    - `planilha/`: Pasta para arquivos CSV
    - `data_by_nap.json`: Dados processados