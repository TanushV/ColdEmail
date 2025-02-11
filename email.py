import requests
import json
from dotenv import load_dotenv
import os

class EmailSender:
    def __init__(self, sender, recipient, subject, text_body):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.text_body = text_body
        self.api_key = self._load_api_key()
        
    def _load_api_key(self):
        load_dotenv()
        api_key = os.getenv('SMTP2GO_API_KEY')
        if not api_key:
            raise Exception("SMTP2GO_API_KEY not found in .env file")
        return api_key

    def send(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            'api_key': self.api_key,
            'sender': self.sender,
            'to': [self.recipient],
            'subject': self.subject,
            'text_body': self.text_body,
            'tracking': {
                'opens': True,
                'clicks': True
            }
        }
        
        response = requests.post(
            'https://api.smtp2go.com/v3/email/send',
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code != 200:
            raise Exception(f"Email failed to send: {response.text}")
            
        result = response.json()
        if result.get('data', {}).get('succeeded') != 1:
            raise Exception(f"Email delivery failed: {result.get('data', {}).get('error')}")
            
        return True

# Example usage:
if __name__ == "__main__":
    email = EmailSender(
        sender="your@domain.com",
        recipient="client@example.com",
        subject="Test with Tracking",
        text_body="This email contains tracking features\nhttps://example.com"
    )
    email.send()
