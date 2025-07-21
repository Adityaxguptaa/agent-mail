from fastapi import FastAPI, BackgroundTasks
from gmail_reader import get_gmail_service, check_latest_email
from whatsapp_sender import send_whatsapp_message
import asyncio
import os
import base64

app = FastAPI()

# ✅ Step 1: Decode credentials.json from env variable if not exists
if not os.path.exists("credentials.json"):
    encoded_creds = os.environ.get("GMAIL_CREDS")
    if not encoded_creds:
        raise Exception("GMAIL_CREDS environment variable not set!")
    with open("credentials.json", "wb") as f:
        f.write(base64.b64decode(encoded_creds))

# ✅ Step 2: Get Gmail service (after decoding)
gmail_service = get_gmail_service()

# ✅ Step 3: Email polling loop
@app.on_event("startup")
async def start_email_polling():
    async def poll_emails():
        while True:
            print("Checking email...")
            snippet = check_latest_email(gmail_service)
            if snippet:
                send_whatsapp_message(f"New Email:\n{snippet}")
            await asyncio.sleep(60)  # Check every 60 seconds

    asyncio.create_task(poll_emails())

# ✅ Step 4: Root route
@app.get("/")
def root():
    return {"status": "Email-to-WhatsApp agent running"}
