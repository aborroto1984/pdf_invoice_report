db_config = {
    "ExampleDb": {
        "server": "example.database.windows.net",
        "database": "ExampleDb",
        "username": "example",
        "password": "example",
        "driver": "{ODBC Driver 17 for SQL Server}",
        "port": 1433,  # Default port for SQL Server
    },
}


def create_connection_string(server_config):
    return (
        f"DRIVER={server_config['driver']};"
        f"SERVER={server_config['server']};"
        f"PORT={server_config["port"]};DATABASE={server_config['database']};"
        f"UID={server_config['username']};"
        f"PWD={server_config['password']}"
    )


sellercloud_credentials = {
    "Username": "username",
    "Password": "password",
}

sellercloud_base_url = "https://example_company.api.sellercloud.us/rest/api/"

sellercloud_endpoints = {
    "GET_SELLERCLOUD_ORDER": {
        "type": "get",
        "url": sellercloud_base_url
        + "Orders?model.orderSourceOrderIDList={ref_id}&model.pageSize=50",
        "endpoint_error_message": "while getting sellercloud_id from SellerCloud: ",
        "success_message": "Sucess!!",
    },
    "GET_TOKEN": {
        "type": "post",
        "url": sellercloud_base_url + "token",
        "endpoint_error_message": "while getting SellerCoud API access token: ",
        "success_message": "Got SellerCloud API access token successfully!",
    },
}

SENDER_EMAIL = "sender_email@domain.com"
SENDER_PASSWORD = "sender_password"
RECIPIENT_EMAILS = [
    "recipient_email_1@domain.com",
    "recipient_email_2@domain.com",
]  # List of emails to send the report
PDF_RECIPIENT_EMAILS = [
    "pdf_recipient_email_1@domain.com",
    "pdf_recipient_email_2@domain.com",
]  # List of emails to send the PDF invoice report
