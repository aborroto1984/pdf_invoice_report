from email_helper import send_email, send_pdf_invoice
from example_db import ExampleDb
from seller_cloud_api import SellerCloudAPI
from helpers import Helpers
from pdf_creator import InvoiceGenerator
from datetime import datetime
from spinner import Spinner
import traceback
import os


def main():
    try:
        spinner = Spinner()
        rc_db = ExampleDb()
        h = Helpers()
        sc_api = SellerCloudAPI()
        tmp_folder = "tmp_pdfs"

        orders_without_pdf, ref_numbers = rc_db.get_orders_without_pdf(spinner)

        if not ref_numbers:
            print("No orders without PDFs found. Exiting script.")
            return

        sellercloud_orders = h.get_sellercloud_order(ref_numbers, sc_api, spinner)

        pdf_creator = InvoiceGenerator()
        all_pdf_data = pdf_creator.create_pdf_data(
            orders_without_pdf, sellercloud_orders, spinner
        )

        all_pdf_invoices = []

        spinner.start("Generating PDF invoices...")
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)

        for pdf_data in all_pdf_data:
            file_name = f"{tmp_folder}\\{pdf_data['reference']}_{datetime.now().strftime('%m_%d_%Y')}.pdf"
            pdf_creator.generate_invoice(pdf_data, file_name)
            rc_db.update_status(pdf_data["reference"])
            all_pdf_invoices.append(file_name)
        spinner.stop()

        spinner.start("Sending PDF invoices...")
        send_pdf_invoice(
            "Company PDF Invoices",
            "Attached are the latest Company PDF invoices.",
            all_pdf_invoices,
        )
        spinner.stop()

        spinner.start("Cleaning up PDF invoices...")
        for pdf in all_pdf_invoices:
            pdf_creator.delete_invoice(pdf)
        spinner.stop()

        print("Script completed successfully.")

    except Exception as e:
        print(
            f"An error occurred while running the Dropship SellerCloud API script. Error message: {str(e)}"
        )
        send_email("An Error Occurred", f"Error: {e}\n\n{traceback.format_exc()}")


if __name__ == "__main__":
    main()
