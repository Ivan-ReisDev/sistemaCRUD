from tkinter import *;
from tkinter import ttk
import customtkinter as ctk
from PIL import Image;
from database import *;
from tkinter import messagebox
import sqlite3;

banco = sqlite3.connect('database_produtos.db');
cursor = banco.cursor();

def read():
    cursor.execute("SELECT * FROM produtos ORDER by nome")
    retorno = cursor.fetchall();
    return retorno

def buscador():
    cleanTab()
    try:
        buscar = str(buscadorEntry.get());
        cursor.execute(f"SELECT * FROM produtos WHERE nome LIKE '{buscar}%'");
        retorno = cursor.fetchall();
        for r in retorno:   
            tabela.insert("","end", values=(r[0],r[1], r[2] ,r[3],r[4],f"R$ {r[5]:,.2f}" ))
        buscadorEntry.delete(0, "end");
    except:
        messagebox.showinfo("ERRO", message="Produto não existe")

def ordernar():
    cursor.execute("SELECT * FROM produtos ORDER by descricao")
    retorno = cursor.fetchall();
    return retorno

def todosProdutos():
     cleanTab()
     res = read()
     for r in res:   
        tabela.insert("","end", values=(r[0],r[1], r[2] ,r[3],r[4],f"R$ {r[5]:,.2f}" ))

def validadorId():
    readId = read();
    list_id = []

    for id in readId:
        list_id.append(int(id[0]))

    idPosicao = len(list_id)
    if idPosicao > 0:
        numeroGerado = max(list_id) + 1
        print(list_id)
        print(numeroGerado)
        return numeroGerado
    else:
        return 1
    
def insert():
    try:
        nomep= str(nomeProduto.get());
        descricaop = str(descricaoProduto.get())
        informacaop = str(informacoesProduto.get())
        estoquep = int(qtdEmEstoque.get())
        precop = float(precoProduto.get())

        if not informacaop:
            cursor.execute(f"INSERT INTO produtos VALUES({validadorId()},'{nomep}', '{descricaop}', '-', {estoquep}, {precop})");
        else:
            cursor.execute(f"INSERT INTO produtos VALUES({validadorId()},'{nomep}', '{descricaop}', '{informacaop}', {estoquep}, {precop})");
        banco.commit()
        clean()
        return
    except:
        messagebox.showinfo("ERRO", message="Por favor digite todos os campos corretamente")

def update():
    try:
        idSelecionado = idProdutoSelecionado
        nomep= str(nwNomeProduto.get());
        descricaop = str(nwDescricaoProduto.get())
        informacaop = str(nwInformacoesProduto.get())
        estoquep = int(nwQtdEmEstoque.get())
        precop = float(nwPrecoProduto.get())

        cursor.execute(f"UPDATE produtos SET nome = '{nomep}' WHERE id = {idSelecionado}");
        cursor.execute(f"UPDATE produtos SET descricao = '{descricaop}' WHERE id = {idSelecionado}");
        cursor.execute(f"UPDATE produtos SET informacoes = '{informacaop}' WHERE id = {idSelecionado}");
        cursor.execute(f"UPDATE produtos SET estoque = {estoquep} WHERE id = {idSelecionado}");
        cursor.execute(f"UPDATE produtos SET preco = '{precop}' WHERE id = {idSelecionado}");
        banco.commit()
        messagebox.showinfo("Sucesso", message="Atualização feita com sucesso");
        new_windows.destroy()
    
    except: 
        new_windows.destroy()
        messagebox.showinfo("ERRO", message="Por favor, preencha todos os dados corretamente");

def cleanTab():
    tabela.delete(*tabela.get_children())

def clean():
    nomeProduto.delete(0, "end");
    descricaoProduto.delete(0, "end");
    informacoesProduto.delete(0, "end");
    qtdEmEstoque.delete(0, "end");
    precoProduto.delete(0, "end");

def delete():
        try:
            valoresNum = obterId()
            itemSelecionado = tabela.selection()[0];
            tabela.delete(itemSelecionado);
            cursor.execute(f"DELETE from produtos WHERE id = {valoresNum}")
            banco.commit()
            new_windows_delete.destroy()
            messagebox.showinfo("Sucesso", message="Produto excluido com sucesso.");
        except:
            new_windows_delete.destroy()
            messagebox.showinfo("ERRO", message="Ocorreu um erro inesperado");

def janelaDelete():
    try:
        global new_windows_delete
        new_windows_delete = ctk.CTkToplevel(main.tab("Produtos"))
        new_windows_delete.geometry("250x100")
        new_windows_delete.iconbitmap("img/icone.ico");
        new_windows_delete.focus_force()
        new_windows_delete.grab_set()
        produtoConfirmacao = produtoUpdate()
        ctk.CTkLabel(new_windows_delete, text=f"Deseja exluir o produto {produtoConfirmacao[1]} ?").place(x=10, y=20)
        ctk.CTkButton(new_windows_delete, text="Sim", fg_color="#008000", corner_radius=0,command=delete).place(x=50, y=50)
    except:
        messagebox.showinfo("ERRO", message="Ocorreu um erro inesperado");

def obterId():
    itemSelecionado = tabela.selection()[0];
    valores = tabela.item(itemSelecionado, "values");
    valorFinal = int(valores[0])
    valorFinal = valorFinal
    return valorFinal

def produtoUpdate():
    itemSelecionado = tabela.selection()[0];
    valores = tabela.item(itemSelecionado, "values");
    return valores;

def verificarProduto():
    lista_num = []
    id = read()
    cont = 0
    for num in id:
        lista_num.append(num[0])
        cont = cont + 1; 

def windowsUpdate():
    try:
        global new_windows
        new_windows = ctk.CTkToplevel(main.tab("Produtos"))
        selecionado = produtoUpdate()
        new_windows.geometry("500x450")
        new_windows.focus_force()
        new_windows.grab_set()
        
        global idProdutoSelecionado, nwNomeProduto, nwDescricaoProduto, nwInformacoesProduto, nwQtdEmEstoque, nwPrecoProduto
        
        idProdutoSelecionado = selecionado[0]
        ctk.CTkLabel(new_windows, text="Atualizar produto", font=("roboto", 20, "bold")).place(x=150, y=50)
        nwNomeProduto = ctk.CTkEntry(new_windows, width=300,corner_radius=0,placeholder_text="Digite o nome do produto")
        nwNomeProduto.insert(0, f"{selecionado[1]}")
        nwNomeProduto.place(x=170, y=100);
        ctk.CTkLabel(new_windows, text="Produto:", font=("roboto", 15, "bold"), ).place(x=50, y=100);

        nwDescricaoProduto = ctk.CTkEntry(new_windows, width=300,corner_radius=0,placeholder_text="Descrição do produto")
        nwDescricaoProduto.place(x=170, y=150)
        nwDescricaoProduto.insert(0, f"{selecionado[2]}")
        ctk.CTkLabel(new_windows, text="Descrição", font=("roboto", 15, "bold"), ).place(x=50, y=150);

        nwInformacoesProduto = ctk.CTkEntry(new_windows, width=300,corner_radius=0,placeholder_text="Informações adicionais (Opcional)")
        nwInformacoesProduto.place(x=170, y=200)
        nwInformacoesProduto.insert(0, f"{selecionado[3]}")
        ctk.CTkLabel(new_windows, text="Informações:", font=("roboto", 15, "bold"), ).place(x=50, y=200);

        nwQtdEmEstoque = ctk.CTkEntry(new_windows, width=300,corner_radius=0,placeholder_text="Quantidade em Estoque")
        nwQtdEmEstoque.place(x=170, y=250);
        nwQtdEmEstoque.insert(0, f"{selecionado[4]}")
        ctk.CTkLabel(new_windows, text="Estoque:", font=("roboto", 15, "bold"), ).place(x=50, y=250);

        nwPrecoProduto = ctk.CTkEntry(new_windows, width=300,corner_radius=0,placeholder_text="Preço do produto")
        nwPrecoProduto.place(x=170, y=300);
        nwPrecoProduto.insert(0, f"{selecionado[5]}")
        ctk.CTkLabel(new_windows, text="Preço:", font=("roboto", 15, "bold"), ).place(x=50, y=300);
        ctk.CTkButton(new_windows, text="Atualizar", corner_radius=0, fg_color="#008000", border_width=1, command=update).place(x=200, y=350);
        new_windows.mainloop();
    except:
        messagebox.showinfo("Erro", message="Selecione um produto")
janela = ctk.CTk();
janela.geometry("1000x600");
janela.title("Sistema de Estoque v.Beta - Desenvolvido por Ivan Reis");
janela.iconbitmap("img/icone.ico");

ctk.CTkLabel(janela, text="Produtos" ,font=("roboto", 30, "bold"), text_color="#ffffff", fg_color="#f59f00").place(x=190, y=80);

imgLogo = ctk.CTkImage(light_image=Image.open("./img/icone.png"), dark_image=Image.open("./img/icone.png"), size=(60,60))
ctk.CTkLabel(janela, text=None, image=imgLogo).place(x=60, y=2);
buscadorEntry = ctk.CTkEntry(janela, width=300, height=35, corner_radius=0, placeholder_text="Escreva o nome do produto...");
buscadorEntry.place(x=180, y=15);
btnSearch = ctk.CTkButton(janela, text="Buscar", width=80,font=("roboto",13,"bold"),height=35, corner_radius=0, fg_color="#d48a02",hover_color="#b67602", command=buscador).place(x=480, y=15);
btnNovoProduto = ctk.CTkButton(janela, text="Novo Produto", corner_radius=0, font=("roboto",13,"bold"), height=35, fg_color="#008000",hover_color="#005c00").place(x=825, y=15);


imgSearch = ctk.CTkImage(light_image=Image.open("./img/search.png"), dark_image=Image.open("./img/search.png"), size=(25,25))

#---------------------- MENU ----------------------

main = ctk.CTkTabview(janela, width=1000, height=540, corner_radius=0, segmented_button_fg_color="#f59f00", border_width=0, segmented_button_selected_color="#945400", segmented_button_unselected_color="#b67602", segmented_button_selected_hover_color="#945400");
main.place(x=0, y=60)

main.add("Cadastro")
main.tab("Cadastro").grid_columnconfigure(0, weight=1)
main.add("Produtos")
main.tab("Produtos").grid_columnconfigure(50, weight=1)


ctk.CTkLabel(main.tab("Cadastro"), width=1500, height=70, text=None, fg_color="#f59f00" ).place(x=0, y=0);
ctk.CTkLabel(main.tab("Cadastro"), text="Cadastro",text_color="#ffffff", font=("roboto", 30,"bold"), fg_color="#f59f00").place(x=30, y=15);

nomeProduto = ctk.CTkEntry(main.tab("Cadastro"), width=300,corner_radius=0,placeholder_text="Digite o nome do produto")
nomeProduto.place(x=400, y=100);
ctk.CTkLabel(main.tab("Cadastro"), text="Produto:", font=("roboto", 15, "bold"), ).place(x=250, y=100);

descricaoProduto = ctk.CTkEntry(main.tab("Cadastro"), width=300,corner_radius=0,placeholder_text="Descrição do produto")
descricaoProduto.place(x=400, y=150)
ctk.CTkLabel(main.tab("Cadastro"), text="Descrição", font=("roboto", 15, "bold"), ).place(x=250, y=150);

informacoesProduto = ctk.CTkEntry(main.tab("Cadastro"), width=300,corner_radius=0,placeholder_text="Informações adicionais (Opcional)")
informacoesProduto.place(x=400, y=200)
ctk.CTkLabel(main.tab("Cadastro"), text="Informações:", font=("roboto", 15, "bold"), ).place(x=250, y=200);

qtdEmEstoque = ctk.CTkEntry(main.tab("Cadastro"), width=300,corner_radius=0,placeholder_text="Quantidade em Estoque")
qtdEmEstoque.place(x=400, y=250);
ctk.CTkLabel(main.tab("Cadastro"), text="Estoque:", font=("roboto", 15, "bold"), ).place(x=250, y=250);

precoProduto = ctk.CTkEntry(main.tab("Cadastro"), width=300,corner_radius=0,placeholder_text="Preço do produto")
precoProduto.place(x=400, y=300);
ctk.CTkLabel(main.tab("Cadastro"), text="Preço:", font=("roboto", 15, "bold"), ).place(x=250, y=300);


ctk.CTkButton(main.tab("Cadastro"), text="Cadastrar", corner_radius=0, fg_color="#008000", border_width=1, command=insert).place(x=400, y=350);
ctk.CTkButton(main.tab("Cadastro"), text="Limpar", corner_radius=0, fg_color="#8b0000", border_width=1, command=clean).place(x=550, y=350);


#---------------------- TABELA PRODUTO ----------------------

ctk.CTkLabel(main.tab("Produtos"), width=1500, height=70, text=None, fg_color="#f59f00" ).place(x=0, y=0);
ctk.CTkLabel(main.tab("Produtos"), text="Produtos",text_color="#ffffff", font=("roboto", 30,"bold"), fg_color="#f59f00").place(x=20, y=15);

btnAtualizaProduto = ctk.CTkButton(main.tab("Produtos"), text="Atualizar", width=80,font=("roboto",13,"bold"), corner_radius=0, fg_color="#d48a02",hover_color="#b67602", command=windowsUpdate).place(x=350, y=95);
TodosProdutos = ctk.CTkButton(main.tab("Produtos"), text="Todos os produtos", width=80,font=("roboto",13,"bold"), corner_radius=0, fg_color="#d48a02",hover_color="#b67602",command=todosProdutos).place(x=440, y=95);
ctk.CTkButton(main.tab("Produtos"), text="Deletar", width=80,font=("roboto",13,"bold"), corner_radius=0, fg_color="#8b0000",hover_color="#b67602",command=janelaDelete).place(x=580, y=95);
     
tabela = ttk.Treeview(main.tab("Produtos"), columns=("id", "produto", "descricao", "informacoes", "estoque", "preco"), show="headings");
tabela.column("id", minwidth=0, width=50)
tabela.column("produto", minwidth=0, width=250)
tabela.column("descricao", minwidth=0, width=250)
tabela.column("informacoes", minwidth=0, width=250)
tabela.column("estoque", minwidth=0, width=100)
tabela.column("preco", minwidth=0, width=100)
tabela.heading("id", text="ID")
tabela.heading("produto", text="Produtos")
tabela.heading("descricao", text="Descrição")
tabela.heading("informacoes", text="Informações")
tabela.heading("preco", text="Preço")
tabela.heading("estoque", text="Estoque")
tabela.place(x=0, y=150, height=500)
janela.mainloop();