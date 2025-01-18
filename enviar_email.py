import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime

# Configurações do email
remetente = "dev.brunodias@gmail.com"  # Substitua pela sua senha de app do Gmail
senha = "Python>JAVA10!"  # Substitua pela sua senha de app do Gmail

destinatarios = [
    "PauloFreitas@itaiquara.com.br",
    "Luciano@itaiquara.com.br",
    "alexandar@itaiquara.com.br"
]

# Criar mensagem
msg = MIMEMultipart()
msg['From'] = remetente
msg['To'] = ", ".join(destinatarios)
msg['Subject'] = "Orçamento - KML ITAIQUARA"

# Corpo do email
corpo_email = """
Prezados,

Segue em anexo o orçamento para o projeto KML ITAIQUARA 2.0.

Ficamos à disposição para quaisquer esclarecimentos adicionais.

Atenciosamente,
"""

msg.attach(MIMEText(corpo_email, 'plain'))

# Anexar o arquivo
arquivo = 'Orçamento KML ITAIQUARA.docx'
with open(arquivo, 'rb') as f:
    part = MIMEApplication(f.read(), Name=os.path.basename(arquivo))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(arquivo)}"'
    msg.attach(part)

# Enviar email
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remetente, senha)
    server.send_message(msg)
    server.quit()
    print("Email enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar email: {str(e)}")
