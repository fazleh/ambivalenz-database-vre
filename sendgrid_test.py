import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def test_sendgrid():
    try:
        sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])

        message = Mail(
            from_email="fazleh2010@gmail.com",   # EXACT verified sender
            to_emails="fazleh2010@gmail.com",    # Recipient (can be same)
            subject="SendGrid Test Email",
            plain_text_content="This is a SendGrid test. ✅",
            html_content="<strong>This is a SendGrid test. ✅</strong>"
        )

        response = sg.send(message)
        print("Status code:", response.status_code)
        print("Response headers:", response.headers)

    except Exception as e:
        print("❌ ERROR")
        print(e)
        if hasattr(e, "body"):
            print("Body:", e.body)

if __name__ == "__main__":
    test_sendgrid()
