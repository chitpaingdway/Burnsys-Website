import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Burnsys Client Auto-Reply (Professional Design Modified) ---
def send_reply_to_client(user_data):
    sender_email = "chit.paingdway@gmail.com"
    sender_password = "uygdjuldmiwdfhbh" 
    client_email = user_data.get('email')

    if not client_email:
        return False

    msg = MIMEMultipart('related')
    msg['Subject'] = "Inquiry Received | Burnsys Technology Dubai"
    msg['From'] = f"Burnsys Technology <{sender_email}>"
    msg['To'] = client_email

    # HTML content ကို Box style နဲ့ Footer အောက်ခြေအချက်အလက်တွေပါအောင် ပြင်ဆင်ထားသည်
    html_content = f"""
    <html>
    <head>
        <style>
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #ffffff;
                border: 1px solid #eeeeee;
                border-radius: 16px;
                overflow: hidden;
            }}
            /* ၁။ Top Bar Background Color */
            .top-bar {{
                background-color: #f5f5f7; /* Apple Style Light Gray */
                padding: 40px 20px;
                text-align: center;
            }}
            .main-content {{
                padding: 40px 30px;
                color: #1d1d1f;
                line-height: 1.8;
            }}
            .footer-contact {{
                background-color: #f9f9f9;
                padding: 30px;
                border-top: 2px solid #FF9500;
                font-size: 14px;
                color: #555555;
            }}
            .contact-row {{
                margin-bottom: 8px;
            }}
            .contact-row strong {{
                color: #1d1d1f;
                width: 70px;
                display: inline-block;
            }}
        </style>
    </head>
    <body style="background-color: #ffffff; margin: 0; padding: 0;">
        <div class="email-container">
            <div class="top-bar">
                <img src="cid:logo_image" alt="Burnsys" style="max-height: 55px;">
            </div>

            <div class="main-content">
                <h2 style="color: #FF9500; margin-top: 0; font-size: 22px;">Dear {user_data.get('name', 'Valued Client')},</h2>
                <p>Thank you for reaching out to <strong>Burnsys Security First</strong>. We have successfully received your inquiry regarding <span style="color: #FF9500; font-weight: bold;">{user_data.get('service')}</span>.</p>
                <p>Our technical experts in Dubai are currently reviewing your requirements. We aim to provide a tailored solution that fits your business needs within 24 hours.</p>
                
                <div style="margin-top: 30px;">
                    <p style="margin: 0; font-weight: bold;">Secure Regards,</p>
                    <p style="margin: 5px 0 0 0; font-size: 18px; color: #FF9500; font-weight: 800;">Burnsys Team</p>
                </div>
            </div>

            <div class="footer-contact">
                <div class="contact-row">
                    <strong>Email:</strong> Hello@burnsys.io
                </div>
                <div class="contact-row">
                    <strong>Phone:</strong> +971 52 355 7541
                </div>
                <div class="contact-row">
                    <strong>Address:</strong> XL Tower Room 502, Marasi Drive, Business Bay, Dubai, UAE
                </div>
                <div style="margin-top: 20px; text-align: center; font-size: 11px; color: #999; border-top: 1px solid #ddd; padding-top: 15px;">
                    © 2026 Burnsys Technology | All rights reserved.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Logo ပုံကို Attachment အနေနဲ့ ပို့ပေးခြင်း (cid:logo_image နဲ့ ချိတ်ဆက်ထားသည်)
        with open('static/logo.png', 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<logo_image>')
            msg.attach(img)
    except Exception as e:
        print(f"Logo Attachment Error: {e}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, client_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Client Reply Error: {e}")
        return False
    

# --- Admin Notification (Internal Lead) ---
def send_email_to_admin(user_data):
    sender_email = "chit.paingdway@gmail.com"
    sender_password = "uygdjuldmiwdfhbh"
    receiver_email = "chit.dwe@burnsys.io"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🚀 NEW LEAD: {user_data.get('name')} | {user_data.get('service')}"
    msg['From'] = f"Burnsys Web Lead <{sender_email}>"
    msg['To'] = receiver_email

    html_content = f"""
    <html>
    <body style="font-family: sans-serif; padding: 20px; background-color: #f0f0f0;">
        <div style="max-width: 500px; margin: auto; background: white; border-top: 5px solid #FF9500; padding: 30px; border-radius: 10px;">
            <h2 style="color: #1d1d1f;">New Business Inquiry</h2>
            <hr style="border: 0; border-top: 1px solid #eee;">
            <p><strong>Name:</strong> {user_data.get('name')}</p>
            <p><strong>Email:</strong> {user_data.get('email')}</p>
            <p><strong>Phone:</strong> {user_data.get('phone')}</p>
            <p><strong>Service:</strong> {user_data.get('service')}</p>
            <p><strong>Message:</strong><br>{user_data.get('description')}</p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Admin Alert Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-started', methods=['POST'])
def get_started():
    # 🛠 FIX: "Unsupported Media Type" ဖြစ်ခြင်းကို ကာကွယ်ရန် နည်းလမ်းမျိုးစုံဖြင့် Data ကို ဖတ်ခြင်း
    if request.is_json:
        data_raw = request.get_json()
    elif request.form:
        data_raw = request.form
    else:
        # fallback for other content types
        data_raw = request.values

    # Data dictionary ကို သေသေချာချာ တည်ဆောက်ခြင်း
    data = {
        'name': data_raw.get('name') or data_raw.get('fullname'),
        'email': data_raw.get('email'),
        'phone': data_raw.get('phone') or data_raw.get('mobile'),
        'service': data_raw.get('service') or 'General Inquiry',
        'description': data_raw.get('description') or data_raw.get('message') or 'No message provided'
    }
    
    # Required data ရှိမရှိ စစ်ဆေးခြင်း
    if not data['email'] or not data['name']:
        return jsonify({"status": "error", "message": "Name and Email are required!"}), 400

    # 1. Admin ဆီ lead ပို့မယ်
    admin_success = send_email_to_admin(data)
    
    if admin_success:
        # 2. Client ဆီ auto-reply ပို့မယ်
        send_reply_to_client(data) 
        return jsonify({"status": "success", "message": "Thank you! Our Dubai team will contact you soon."}), 200
    else:
        return jsonify({"status": "error", "message": "Server encountered an issue. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)