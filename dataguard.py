# DataGuard - Ferramenta de Anonimização de Dados Sensíveis
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from faker import Faker

fake = Faker()

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
        elif 'cpf' in coluna.lower():
            df[coluna] = ['***' for _ in range(len(df))]
        elif 'email' in coluna.lower():
            df[coluna] = ['***' for _ in range(len(df))]
        elif 'telefone' in coluna.lower():
            df[coluna] = ['***' for _ in range(len(df))]
        elif 'endereco' in coluna.lower():
            df[coluna] = ['***' for _ in range(len(df))]
        elif 'data_nascimento' in coluna.lower():
            df[coluna] = ['***' for _ in range(len(df))]
        else:
            df[coluna] = '***'
    return df

def carregar_arquivo():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip()

        colunas = detectar_colunas_sensiveis(df)

        if not colunas:
            messagebox.showinfo("DataGuard", "Nenhuma coluna sensível detectada.")
            return

        df_anonimizado = anonimizar_dados(df.copy(), colunas)

        mostrar_resultados(df, df_anonimizado)

    except Exception as e:
        messagebox.showerror("Erro", str(e))

def salvar_arquivo(df):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        df.to_csv(save_path, index=False, sep=';')
        messagebox.showinfo("DataGuard", "Arquivo anonimizado salvo com sucesso!")

def mostrar_resultados(original, anonimizado):
    resultado = tk.Toplevel()
    resultado.title("Resultados da Anonimização")
    resultado.geometry("1000x600")

    frame_top = tk.Frame(resultado, pady=10)
    frame_top.pack()

    botao_salvar = tk.Button(frame_top, text="Salvar Arquivo Anonimizado", command=lambda: salvar_arquivo(anonimizado))
    botao_salvar.pack()

    label_percentual = tk.Label(frame_top)
    label_percentual.pack()

    frame_tables = tk.Frame(resultado)
    frame_tables.pack(expand=True, fill='both')

    frame_original = tk.Frame(frame_tables, padx=10)
    frame_original.pack(side='left', expand=True, fill='both')
    frame_anonimizado = tk.Frame(frame_tables, padx=10)
    frame_anonimizado.pack(side='left', expand=True, fill='both')

    label1 = tk.Label(frame_original, text="Original")
    label1.pack()
    tree_original = ttk.Treeview(frame_original)
    tree_original.pack(expand=True, fill='both')

    tree_original['columns'] = list(original.columns)
    for coluna in original.columns:
        tree_original.heading(coluna, text=coluna)
        tree_original.column(coluna, anchor='center')

    for _, row in original.iterrows():
        tree_original.insert("", "end", values=list(row))

    label2 = tk.Label(frame_anonimizado, text="Anonimizado")
    label2.pack()
    tree_anonimizado = ttk.Treeview(frame_anonimizado)
    tree_anonimizado.pack(expand=True, fill='both')

    tree_anonimizado['columns'] = list(anonimizado.columns)
    for coluna in anonimizado.columns:
        tree_anonimizado.heading(coluna, text=coluna)
        tree_anonimizado.column(coluna, anchor='center')

    for _, row in anonimizado.iterrows():
        tree_anonimizado.insert("", "end", values=list(row))

    percentual = (len(anonimizado.columns) / len(original.columns)) * 100
    label_percentual.config(text=f"{percentual:.2f}% das colunas foram anonimizadas.")

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

app.mainloop()