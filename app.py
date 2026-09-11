import os
import mysql.connector
import smtplib
import subprocess
import time
from email.mime.text import MIMEText

conexao = mysql.connector.connect(
    host=os.getenv("CHAVE"),
    user=os.getenv("DB_USUARIO"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DATA")
)
cursor = conexao.cursor()
print("-"*20)
print("              SOUCEX")
print("   Melhore sua Rotina com Automações")
print("-"*20)
print('\n')
print("Bem vindo a SOUCEX")
print("Software de Automações que melhoram sua rotina e seu desempenho")
print('\n')
while True:
    def sair():
        print("obrigado por usar o sistema")
        exit()
    def inicio():
        escolha = input("""Opções
        1. Iniciar Automações
        2. Faça suas Automações
        3. Personalização
        4. Sair
        Escolha uma opção acima pelo número correspondente: """)
        if escolha == "1":
            iniciar()
        elif escolha == "2":
            fazer_automacao()
        elif escolha == "3":
            personalizar()
        elif escolha == "4":
            sair()

        return True
    def abrir(nome):
        if nome.startswith(("http://", "https://")):
            subprocess.Popen(["xdg-open", nome])
            return
        for raiz, pastas, arquivos in os.walk("/home/zorin"):
            if nome in arquivos:
                caminho = os.path.join(raiz, nome)
                subprocess.Popen(["xdg-open", caminho])
                return

        print("Não encontrei:", nome)
    def personalizar():
        while True:
            opcao = input(""" Opções:
            1. Ver Automações
            2. Excluir Automação
        """)
            if opcao == "1":
                cursor.execute("SELECT comando FROM automacao WHERE id_usuario = %s", (id_usuario,))
                v0 = cursor.fetchall()
                cursor.execute("SELECT email_usuario, email_titulo, email_mensagem, email_to, chave FROM gmail WHERE id_usuario = %s", (id_usuario,))
                v1 = cursor.fetchall()
                print("Automação de arquivos")
                print("")
                for i in v0:
                    print(f"{i[0]}")
                print("-"*20)
                print("Gmail")
                for i in v1:
                    print(f"""
        Email: {i[0]}
        Título: {i[1]}
        Mensagem: {i[2]}
        Para: {i[3]}
        Chave: {i[4]}
        """)
            elif opcao == "2":
                while True:
                    perg = input("""Qual quer excluir:
                    1. Arquivos
                    2. Email
                    """)
                    if perg == "1":
                        qual = input("Coloque o nome do arquivo para excluir: ")
                        cursor.execute("DELETE FROM automacao WHERE comando = %s", (qual,))
                        conexao.commit()
                    elif perg == "2":
                        q = input("Coloque o titulo do email: ")
                        cursor.execute("DELETE FROM gmail WHERE email_titulo = %s", (q,))
                        conexao.commit()
                        print(f"Sucesso, Email Deletado: {q}")
                    elif perg == "exit":
                        inicio()
                    else:
                        print("Selecione só números 1 e 2")
            elif opcao == "exit":
                inicio()
            else:
                print("Se quiser voltar para o inicio use, exit")
    def iniciar():
        cursor.execute("SELECT comando FROM automacao WHERE id_usuario = %s", (id_usuario,))
        v = cursor.fetchall()
        for vs in v:
            abrir(vs[0])
        cursor.execute("""
            SELECT email_usuario, email_titulo, email_mensagem, email_to, chave
            FROM gmail
            WHERE id_usuario = %s
        """, (id_usuario,))

        emails = cursor.fetchall()
        if emails:
            for email in emails:
                remetente = email[0]
                titulo = email[1]
                texto = email[2]
                destinatario = email[3]
                chave = email[4]

                mensagem = MIMEText(texto)
                mensagem["Subject"] = titulo
                mensagem["From"] = remetente
                mensagem["To"] = destinatario

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
                servidor.login(remetente, chave)
                servidor.send_message(mensagem)
        else:
            print("")
        time.sleep(0.5)
        inicio()
        
    def fazer_automacao():
        print(" Crie uma Automação")
        while True:
            que = input("""O que quer Automatizar
            1. Aplicativo
            2. Site
            3. Musica
            4. Email
            5. Sair
            """)
            if que == "1":
                app = input("Arraste o arquivo do aplicativo aqui: ")
                if app.replace == "":
                    print("Deixe um arquivo! ou saia digitando exit")
                elif app.replace == "exit":
                    print("Saiu")
                else:
                    cursor.execute("INSERT INTO automacao (id_usuario, comando) VALUES (%s, %s)", (id_usuario, app))
                    conexao.commit()
                    print("Pronto")
            elif que == "2":
                app = input("Arraste o endereço do site aqui: ")
                if app.replace == "":
                    print("Deixe o HTTPS! ou saia digitando exit")
                elif app.replace == "exit":
                    print("Saiu")
                else:
                    cursor.execute("INSERT INTO automacao (id_usuario, comando) VALUES (%s, %s)", (id_usuario, app))
                    conexao.commit()
                    print("Pronto")
            elif que == "3":
                app = input("Arraste o arquivo da musica aqui: ")
                if app.replace == "":
                    print("Deixe um arquivo! ou saia digitando exit")
                elif app.replace == "exit":
                    print("Saiu")
                else:
                    cursor.execute("INSERT INTO automacao (id_usuario, comando) VALUES (%s, %s)", (id_usuario, app))
                    conexao.commit()
                    print("Pronto")
            elif que == "4":
                email = input("Digite o email que vai Enviar a Mensagem: ")
                email_recebido = input("Digite o email que vai Receber a Mensagem: ")
                email_titulo = input("Digite o título do email: ")
                email_texto = input("Digite o texto do email: ")
                chave = input("Digite a Chave do Email: ")
                cursor.execute("INSERT INTO gmail (id_usuario, email_usuario, email_titulo, email_mensagem, email_to, chave) VALUES (%s, %s, %s, %s, %s, %s)", (id_usuario, email, email_titulo, email_texto, email_recebido, chave))
                conexao.commit()
            elif que == "5":
                inicio()
            else:
                print("Coloque um dos números 1, 2, 3, 4, 5 para cada ação!")

    #-----------------------------------
    pergunta = input("Tem cadastro?(S/N): ")
    if pergunta == "S":
        nome_usuario = input("Insira seu nome: ")
        cursor.execute("SELECT id FROM usuario WHERE nome_usuario = %s", (nome_usuario,))
        v = cursor.fetchall()
        conexao.commit()
        if v:
            print("Sucesso")
            id_usuario = v[0][0]
            inicio()
        else:
            print("nome errado")
    elif pergunta == "N":
        nome_usuario = input("Digite seu nome: ")
        cursor.execute("INSERT INTO usuario (nome_usuario) VALUES (%s)", (nome_usuario,))
        conexao.commit()
        id_usuario = cursor.lastrowid
    elif pergunta == "exit":
        sair()