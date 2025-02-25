# PDF Invoice Generation and Order Management System

This project automates invoice generation, SellerCloud order tracking, and email notifications.

## Features
- Retrieves orders that require PDF invoices.
- Fetches order details from SellerCloud.
- Generates PDF invoices using ReportLab.
- Sends generated invoices via email.
- Updates order statuses in the database.

## Project Structure
```
project_root/
├── config.py              # Configuration file for database, API, and email credentials
├── email_helper.py        # Sends email notifications with PDFs
├── example_db.py          # Manages database interactions
├── helpers.py             # Utility functions for batching and order fetching
├── main.py                # Main script orchestrating invoice generation
├── pdf_creator.py         # Generates PDF invoices
├── seller_cloud_api.py    # Interfaces with SellerCloud API
├── spinner.py             # Provides a terminal-based progress spinner
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/pdf-invoice-generator.git
cd pdf-invoice-generator
```

### 2. Install Dependencies
Ensure you have Python 3 installed, then install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure the System
Modify `config.py` with your database, FTP, and API credentials.

Example database configuration:
```python
db_config = {
    "ExampleDb": {
        "server": "your.database.windows.net",
        "database": "YourDB",
        "username": "your_user",
        "password": "your_password",
        "driver": "{ODBC Driver 17 for SQL Server}",
    },
}
```
Example email configuration:
```python
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_email_password"
PDF_RECIPIENT_EMAILS = ["recipient@example.com"]
```

## Usage
Run the main script to start the invoice generation process:
```bash
python main.py
```

## How It Works
1. Fetches orders needing PDF invoices from the database.
2. Retrieves order details from SellerCloud.
3. Generates formatted PDF invoices.
4. Sends invoices via email.
5. Updates order statuses in the database.

## Tech Stack
- Python 3
- ReportLab (PDF generation)
- Azure SQL Database (`pyodbc`)
- SellerCloud API Integration
- Email Notifications (`smtplib`)

## Troubleshooting
- If you encounter database connection issues, ensure `ODBC Driver 17` is installed.
- If emails fail to send, ensure your SMTP settings allow external authentication.
- Verify SellerCloud credentials if API requests fail.
