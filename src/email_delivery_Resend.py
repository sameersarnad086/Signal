import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def send_email(subject, html_content, to_email):
    params = {
        "from": os.getenv("SIGNAL_FROM_EMAIL"),
        "to": to_email,
        "subject": subject,
        "html": html_content
    }
    
    response = resend.Emails.send(params)
    print(f"Email sent. ID: {response['id']}")
    return response['id']

def format_email_html(bits_text):
    bits = bits_text.split("*Bit ")
    bits = [b for b in bits if b.strip()]
    
    html = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1F4E79; border-bottom: 2px solid #2E75B6; padding-bottom: 10px;">
            Signal's daily AI bits — filtered for what matters to you and your goals.
        </h2>
    """
    
    for bit in bits:
        html += f"""
        <div style="background: #DEEAF1; border-left: 4px solid #2E75B6; 
                    padding: 15px; margin: 15px 0; border-radius: 4px;">
            <p style="color: #1F4E79; font-weight: bold; margin: 0 0 8px 0;">Bit {bit[:bit.find(chr(10))]}</p>
            <p style="color: #1a1a1a; margin: 0; line-height: 1.6;">{bit[bit.find(chr(10)):].strip()}</p>
        </div>
        """
    
    html += """
        <p style="color: #595959; font-size: 12px; border-top: 1px solid #DEEAF1; 
                  padding-top: 10px; margin-top: 20px;">
            Reply with 👍 liked it, 👎 missed the mark, or 💡 teach me more.
        </p>
    </div>
    """
    
    return html