from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Update with your email credentials
EMAIL_ADDRESS = 'srikar.ganesh2004@gmail.com'  # Your email
EMAIL_PASSWORD = 'wmnb pvfg *******'  # Your application password


@app.route('/api/send-mails', methods=['POST', 'OPTIONS'])  # Allow OPTIONS method
def send_mails():
    if request.method == 'OPTIONS':  # Handle preflight OPTIONS request
        response = jsonify({'message': 'CORS preflight successful'})
        response.status_code = 200
        return response


    try:
        data = request.json
        emails = data.get('emails', [])


        if not emails or not isinstance(emails, list):
            return jsonify({'message': 'Invalid email list provided.'}), 400


        # SMTP setup
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587


        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)


            for email in emails:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = email
                msg['Subject'] = "Greeting"
                body = f"The patient has been added to the database."
                msg.attach(MIMEText(body, 'plain'))


                server.send_message(msg)


        return jsonify({'message': 'Emails sent successfully!'}), 200


    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to send emails.'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)