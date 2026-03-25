import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp(message, to_number):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )
    
    chunks = split_message(message)
    sids = []
    
    for i, chunk in enumerate(chunks):
        result = client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
            to=f"whatsapp:{to_number}",
            body=chunk
        )
        print(f"Message {i+1}/{len(chunks)} sent. SID: {result.sid}")
        sids.append(result.sid)
    
    return sids

def split_message(message, limit=1500):
    if len(message) <= limit:
        return [message]
    
    chunks = []
    paragraphs = message.split("\n\n")
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= limit:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
