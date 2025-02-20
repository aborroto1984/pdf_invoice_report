import smtplib
from email.message import EmailMessage
from config import SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAILS, PDF_RECIPIENT_EMAILS
import os
import getpass
import socket


def send_email(subject, body):
    current_dir = os.getcwd()
    folder_name = os.path.basename(current_dir)
    computer_name = socket.gethostname()
    user_name = getpass.getuser()
    new_line = "\n"
    body_with_new_line = (
        f"{body}{new_line}{folder_name} on {computer_name} ({user_name})"
    )
    msg = EmailMessage()
    msg.set_content(body_with_new_line)
    msg["Subject"] = f"{subject} : {folder_name}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENT_EMAILS)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def send_pdf_invoice(subject, body, pdf_paths):
    """
    Send an email with multiple PDF attachments.

    Args:
        subject (str): The email subject.
        body (str): The email body content.
        pdf_paths (list): List of file paths for the PDFs to be attached.
    """
    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(PDF_RECIPIENT_EMAILS)

    # Loop through the list of PDF paths and attach each one
    for pdf_path in pdf_paths:
        try:
            file_name = os.path.basename(pdf_path)
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                # Add the PDF as an attachment
                msg.add_attachment(
                    pdf_data, maintype="application", subtype="pdf", filename=file_name
                )
        except FileNotFoundError:
            print(f"Error: PDF file not found at path: {pdf_path}")
        except Exception as e:
            print(f"Error attaching the file: {pdf_path}. Error: {e}")
            return  # Exit the function if any file fails

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
