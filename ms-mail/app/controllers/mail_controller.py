import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

FROM_MAIL = os.getenv("FROM_MAIL")
PASS_MAIL = os.getenv("PASS_MAIL")

class mailController:
    def enviar_correo(self, contraseña, destinatario, asunto, cuerpo):
        msg = EmailMessage()
        msg['Subject'] = asunto
        msg['From'] = FROM_MAIL
        msg['To'] = destinatario
        msg.set_content(cuerpo)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remitente, contraseña)
                smtp.send_message(msg)
            print("Correo enviado correctamente")
        except Exception as e:
            print(f"Error al enviar correo: {e}")


