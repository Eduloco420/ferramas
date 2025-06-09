import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from flask import jsonify, request

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

FROM_MAIL = os.getenv("FROM_MAIL")
PASS_MAIL = os.getenv("PASS_MAIL")

class mailController:
    def enviar_correo(self):
        data = request.get_json()
        destinatario = data['destinatario']
        asunto = data['asunto']
        cuerpo = data['cuerpo']

        msg = EmailMessage()
        msg['Subject'] = asunto
        msg['From'] = FROM_MAIL
        msg['To'] = destinatario
        msg.set_content("Este correo requiere un cliente que soporte HTML para visualizarlo correctamente.")
        msg.add_alternative(cuerpo, subtype='html')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(FROM_MAIL, PASS_MAIL)
                smtp.send_message(msg)
            return jsonify({'mensaje':'Correo enviado correctamente'}), 200
        except Exception as e:
            return jsonify({'mensaje':'Error enviando correo electronico', 'Error':str(e)}), 400

