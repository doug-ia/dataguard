# DataGuard - Ferramenta de Anonimização de Dados Sensíveis (layout melhorado e centralizado)
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from faker import Faker

fake = Faker()

# Funções principais
def detectar_colunas_sensiveis(df):
    colunas_sensiveis = []
    palavras_chave = ['nome', 'cpf', 'email', 'telefone', 'endereco', 'data_nascimento']
    for coluna in df.columns:
        for palavra in palavras_chave:
            if palavra in coluna.lower():
                colunas_sensiveis.append(coluna)
    return colunas_sensiveis

def anonimizar_dados(df, colunas):
    for coluna in colunas:
        if 'nome' in coluna.lower():
            df[coluna] = ['anonimo' for _ in range(len(df))]
        elif any(chave in coluna.lower() for chave in ['cpf', 'email', 'telefone', 'endereco', 'data_nascimento']):
            df[coluna] = ['***' for _ in range(len(df))]
        else:
            df[coluna] = '***'
    return df

def mostrar_dataframes(df_original, df_anonimizado):
    for widget in frame_dados.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10))

    # Treeview Original
    tree_original = ttk.Treeview(frame_dados)
    tree_original['columns'] = list(df_original.columns)
    tree_original.heading('#0', text='Linha')

    for col in df_original.columns:
        tree_original.heading(col, text=col)
        tree_original.column(col, width=100)

    for idx, row in df_original.iterrows():
        tree_original.insert('', 'end', text=idx, values=list(row))

    scrollbar_y = ttk.Scrollbar(frame_dados, orient='vertical', command=tree_original.yview)
    tree_original.configure(yscrollcommand=scrollbar_y.set)

    # Treeview Anonimizado
    tree_anon = ttk.Treeview(frame_dados)
    tree_anon['columns'] = list(df_anonimizado.columns)
    tree_anon.heading('#0', text='Linha')

    for col in df_anonimizado.columns:
        tree_anon.heading(col, text=col)
        tree_anon.column(col, width=100)

    for idx, row in df_anonimizado.iterrows():
        tree_anon.insert('', 'end', text=idx, values=list(row))

    scrollbar_y2 = ttk.Scrollbar(frame_dados, orient='vertical', command=tree_anon.yview)
    tree_anon.configure(yscrollcommand=scrollbar_y2.set)

    # Layout das tabelas
    lbl1 = tk.Label(frame_dados, text="Original", font=('Arial', 12, 'bold'))
    lbl1.grid(row=0, column=0)
    tree_original.grid(row=1, column=0, sticky='nsew')
    scrollbar_y.grid(row=1, column=1, sticky='ns')

    lbl2 = tk.Label(frame_dados, text="Anonimizado", font=('Arial', 12, 'bold'))
    lbl2.grid(row=0, column=2)
    tree_anon.grid(row=1, column=2, sticky='nsew')
    scrollbar_y2.grid(row=1, column=3, sticky='ns')

    frame_dados.grid_columnconfigure(0, weight=1)
    frame_dados.grid_columnconfigure(2, weight=1)
    frame_dados.grid_rowconfigure(1, weight=1)

def carregar_arquivo():
    global df_original, df_anonimizado

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        df_original = pd.read_csv(file_path, sep=';', encoding='utf-8')
        df_original.columns = df_original.columns.str.strip()

        colunas = detectar_colunas_sensiveis(df_original)
        if not colunas:
            messagebox.showinfo("DataGuard", "Nenhuma coluna sensível detectada.")
            return

        df_anonimizado = anonimizar_dados(df_original.copy(), colunas)
        mostrar_dataframes(df_original, df_anonimizado)

        porcentagem = (len(colunas) / len(df_original.columns)) * 100
        label_status.config(text=f"{len(colunas)} de {len(df_original.columns)} colunas anonimizadas ({porcentagem:.2f}%)")
        

    except Exception as e:
        messagebox.showerror("Erro", str(e))

def salvar_arquivo():
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        df_anonimizado.to_csv(save_path, index=False, sep=';')
        messagebox.showinfo("DataGuard", "Arquivo anonimizado salvo com sucesso!")


# --- Interface Gráfica ---
app = tk.Tk()
app.title("DataGuard - Anonimizador de Dados")
app.geometry("400x250")
app.configure(bg='#4776a1')

frame = tk.Frame(app, bg='#4776a1')
frame.pack(expand=True)

label = tk.Label(frame, text="Bem-vindo ao DataGuard", font=("Helvetica", 16), bg='#4776a1', fg='#f0f0f0')
label.pack(pady=10)

subtitulo = tk.Label(frame, text="Anomizador de Dados", font=("Georgia", 12), bg='#4776a1')
subtitulo.pack(pady=10)

instrucao = tk.Label(frame, text="Clique no botão abaixo para carregar um arquivo CSV.", bg='#f0f0f0', padx=10, pady=5)
instrucao.pack(pady=8)

botao_carregar = tk.Button(frame, text="Carregar Arquivo", command=carregar_arquivo, bg='#4CAF50', fg='white', padx=10, pady=5)
botao_carregar.pack(pady=20)

btn_salvar = tk.Button(frame, text="Salvar Anonimizado", command=salvar_arquivo, bg='#2196F3', fg='white', padx=10, pady=5, state='disabled')
btn_salvar.pack(pady=5)

label_status = tk.Label(app, text="", bg='#4776a1', fg='white')
label_status.pack(pady=5)

frame_dados = tk.Frame(app, bg='#4776a1')
frame_dados.pack(fill='both', expand=True)

# Rodar o app
app.mainloop()
