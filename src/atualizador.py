import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import shutil
from datetime import datetime
import os

def atualizar_planilha(novo_arquivo):
    # Cria pasta de backup se não existir
    if not os.path.exists('backups'):
        os.makedirs('backups')
    
    # Faz backup do arquivo atual
    data_backup = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy2(
        'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv',
        f'backups/backup_{data_backup}.csv'
    )
    
    # Copia novo arquivo
    shutil.copy2(novo_arquivo, 'src/templates/planilha/TRESLAGOAS_MS_378_20251102_GPON (2).csv')
    return True

class AtualizadorPlanilha:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Claro - Atualização de Planilha")
        self.root.geometry("500x400")
        self.root.configure(bg='#333333')
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        frame = tk.Frame(self.root, bg='#333333', padx=30, pady=30)
        frame.pack(expand=True, fill='both')
        
        # Logo (texto temporário)
        logo_label = tk.Label(frame,
                            text="CLARO",
                            font=('Arial', 24, 'bold'),
                            fg='#DA291C',
                            bg='#333333')
        logo_label.pack(pady=20)
        
        # Título
        titulo = tk.Label(frame,
                         text="Sistema de Atualização de Planilha",
                         font=('Arial', 16),
                         fg='white',
                         bg='#333333')
        titulo.pack(pady=20)
        
        # Botão de atualização
        btn_atualizar = tk.Button(frame,
                                text="Selecionar Nova Planilha",
                                command=self.selecionar_arquivo,
                                bg='#DA291C',
                                fg='white',
                                font=('Arial', 12, 'bold'),
                                padx=20,
                                pady=10,
                                relief=tk.FLAT)
        btn_atualizar.pack(pady=20)
        
        # Informações
        info_text = """
        • Sistema faz backup automático dos dados
        • Atualiza a interface de busca
        • Mantém histórico de todas as versões
        • Selecione apenas arquivos CSV
        """
        info = tk.Label(frame,
                       text=info_text,
                       font=('Arial', 11),
                       fg='white',
                       bg='#333333',
                       justify='left')
        info.pack(pady=20)
        
        # Versão
        versao = tk.Label(frame,
                         text="v1.0",
                         font=('Arial', 8),
                         fg='#666666',
                         bg='#333333')
        versao.pack(side='bottom', pady=10)
    
    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(
            title="Selecione o novo arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        
        if arquivo:
            try:
                # Confirma a atualização
                if messagebox.askyesno("Confirmar", "Deseja atualizar a planilha? Será feito um backup automaticamente."):
                    # Tenta atualizar
                    if atualizar_planilha(arquivo):
                        # Executa o script de geração do HTML
                        os.system('python3 src/generate_v2.py')
                        
                        messagebox.showinfo(
                            "Sucesso",
                            "Planilha atualizada com sucesso!\nBackup criado na pasta 'backups'."
                        )
            except Exception as e:
                messagebox.showerror(
                    "Erro",
                    f"Erro ao atualizar planilha: {str(e)}"
                )
    
    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AtualizadorPlanilha()
    app.executar()