from datetime import datetime, date
import inspect
import pyautogui
import webbrowser
from imap_tools import MailBox
from imap_tools import A
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import os

load_dotenv()

class Email:
    def __init__(self):
        self.email = os.getenv("EMAIL")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.imap_email = "imap.gmail.com"

    def read_email(self, seen: bool, limit: int) -> str:
        emails = []
        try:
            with MailBox(self.imap_email).login(self.email, self.email_password) as mailbox:
                for msg in mailbox.fetch(A(seen=seen), limit=limit, reverse=True):
                    text = (f"--- Email --- \n"
                            f"From: {msg.from_}\n"
                            f"Subject: {msg.subject}\n"
                            f"Body: {msg.text}\n"
                            f"Date: {msg.date}\n")
                    emails.append(text)
                return "\n".join(emails) if emails else "no email"
        except Exception as e:
            return str(e)
        
    def send_email(self, to: str, subject: str, body: str) -> str:

        msg = EmailMessage()
        msg["From"] = self.email
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        permission = input(f"Send email to '{to}' with subject '{subject}'? (yes/no): ").lower().strip()
        if permission not in ["yes", "y", "ys"]:
            return "permission denied"
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.email, self.email_password)
                server.send_message(msg)
                return f"Email sent successfully to {to}"
        except Exception as e:
            return f"Failed to send email: {e}"

class TimeStamp:
    @staticmethod
    def get_datetime():
        """Get current date and time."""
        current_date = date.today().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"Current time: {current_time} | Current_date: {current_date}"
    
class OpenApplication():
    @staticmethod
    def open_app(name: str) -> str:
            print(f"opening {name}")
            try:
                pyautogui.hotkey("win", "s")
                pyautogui.write(name, interval=0.05)
                pyautogui.press("enter")
                return "app open success"
            except Exception as e:
                return str(e)
    @staticmethod
    def open_website(name: str) -> str:
        try:
            webbrowser.open(f"https://{name}.com/")
            return "success"
        except Exception as e:
            return str(e)
        
class ToolCall(TimeStamp, OpenApplication, Email):
    def __init__(self):
        super().__init__()
        self.tool_list = [self.get_datetime, self.open_app, self.open_website, self.read_email, self.send_email]
        self.tools = {"get_datetime": self.get_datetime,
                      "open_app": self.open_app,
                      "open_website":self.open_website,
                      "read_email": self.read_email,
                      "send_email": self.send_email}

    def execute_tool(self, tool_name: str, args: dict) -> str:
        if tool_name not in self.tools:
            return "Unknown Tool Name! "
        try:
            tool = self.tools[tool_name]
            sig = inspect.signature(tool)
            clean_args = {k: v for k, v in args.items()
                            if k in sig.parameters}
            return tool(**clean_args)
        except Exception as e:
            return f"tool execution error: {e}"
        

if __name__ == "__main__":
    a = TimeStamp()
    print(a.get_datetime())
        