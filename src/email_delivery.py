import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, html_content, to_email):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": os.getenv("SIGNAL_FROM_EMAIL"), "name": "Signal"},
        subject=subject,
        html_content=html_content
    )

    response = api_instance.send_transac_email(send_smtp_email)
    print(f"Email sent. Message ID: {response.message_id}")
    return response.message_id

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
            P.S. Signal runs on WhatsApp's free tier — your reply keeps Signal running for tomorrow.
        </p>
    </div>
    """

    return html
