from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
import os
from spinner import Spinner
import re


class InvoiceGenerator:
    def __init__(self, logo_path, filename="invoice.pdf"):
        self.logo_path = logo_path
        self.filename = filename
        self.styles = getSampleStyleSheet()

        # Define separate styles for different alignments
        self.left_aligned_style = self.styles["Normal_Left"]
        self.left_aligned_style.alignment = TA_LEFT

        self.right_aligned_style = self.styles["Normal_Right"]
        self.right_aligned_style.alignment = TA_RIGHT

        self.center_aligned_style = self.styles["Normal_Center"]
        self.center_aligned_style.alignment = TA_CENTER

        self.ship_to_address = "Name Last\nShip to Address\nCity, State, Zip, Country"
        self.bill_to_address = "Name Last\nBill to Address\nCity, State, Zip, Country"
        self.company_address = (
            "Selling Company Address\nCity, State Zip\nPhone: (555) 555-5555"
        )

    def _get_logo(self):
        """Add logo or a placeholder"""
        if self.logo_path:
            return Image(self.logo_path, width=73, height=73)
        return Paragraph("", self.styles["Normal"])  # Empty if no logo

    def _get_header_table(self, invoice_data):
        """Create the header table with logo, addresses, and invoice info"""
        bill_to = f"BILL TO:<br/>{self.bill_to_address}"

        left_column_data = [
            [self._get_logo()],
            [Paragraph(self.company_address, self.left_aligned_style)],
            [Spacer(1, 12)],
            [Paragraph(bill_to, self.left_aligned_style)],
        ]
        left_column_table = Table(left_column_data, colWidths=[2.5 * inch])

        # Invoice title and right-aligned content
        tittle_right_aligned_style = self.styles["Title"]
        tittle_right_aligned_style.alignment = TA_RIGHT
        tittle_right_aligned_style.fontSize = 28

        invoice_title = "<b>INVOICE</b>"
        date_and_reference = (
            f"REFERENCE#: {invoice_data['reference']}<br/>DATE: {invoice_data['date']}"
        )
        ship_to = f"SHIP TO:<br/>{self.ship_to_address}"

        right_column_data = [
            [Spacer(1, 12)],
            [Paragraph(invoice_title, tittle_right_aligned_style)],
            [Spacer(1, 12)],
            [Paragraph(date_and_reference, self.right_aligned_style)],
            [Spacer(1, 12)],
            [Paragraph(ship_to, self.right_aligned_style)],
        ]
        right_column_table = Table(right_column_data, colWidths=[2.5 * inch])

        center_column_data = [[""], [""], [Spacer(1, 12)], [""]]
        center_column_table = Table(center_column_data, colWidths=[2.5 * inch])

        # Combine left and right columns into a header table
        header_table = Table(
            [[left_column_table, center_column_table, right_column_table]],
            colWidths=[2.5 * inch, 2.2 * inch, 2.8 * inch],
        )
        header_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
        return header_table

    def _create_invoice_items_table(self, invoice_data):
        """Create the invoice items table"""
        data = [["PO#", "PART#", "QTY", "PART NAME", "UNIT PRICE", "LINE TOTAL"]]

        total_qty = 0
        total_line_sum = 0.0

        for item in invoice_data["items"]:
            data.append(
                [
                    item["po"],
                    item["part"],
                    item["qty"],
                    Paragraph(
                        item["description"], self.left_aligned_style
                    ),  # Left-aligned PART NAME
                    Paragraph(
                        f"${item['unit_price']:,.2f}", self.center_aligned_style
                    ),  # Center-aligned UNIT PRICE
                    Paragraph(
                        f"${item['line_total']:,.2f}", self.center_aligned_style
                    ),  # Right-aligned LINE TOTAL
                ]
            )
            total_qty += item["qty"]
            total_line_sum += item["line_total"]

        # Define column widths
        colWidths = [
            0.8 * inch,
            1.0 * inch,
            0.8 * inch,
            2.8 * inch,
            1.0 * inch,
            1.0 * inch,
        ]

        # Create the main table for the items
        table = Table(data, colWidths=colWidths)

        # Style the table
        table.setStyle(
            TableStyle(
                [
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black,
                    ),  # Grid for all rows
                ]
            )
        )

        return table  # Just return the main table

    def generate_invoice(self, invoice_data, filename):
        """Generate the PDF invoice"""
        pdf = SimpleDocTemplate(filename, pagesize=LETTER)
        elements = []

        # Add the header section
        elements.append(self._get_header_table(invoice_data))
        elements.append(Spacer(1, 12))

        # Add the invoice items table
        elements.append(self._create_invoice_items_table(invoice_data))
        elements.append(Spacer(1, 12))

        # Adding TOTAL and other rows in a separate summary table
        summary_data = [
            [
                "Total",
                "",
                sum(item["qty"] for item in invoice_data["items"]),
                "",
                "SUBTOTAL",
                f"${sum(item['line_total'] for item in invoice_data['items']):,.2f}",
            ],
            ["", "", "", "", "FEES", f"${invoice_data['fees']:,.2f}"],
            [
                "",
                "",
                "",
                "",
                "TOTAL",
                f"${(sum(item['line_total'] for item in invoice_data['items']) + invoice_data['fees']):,.2f}",
            ],
        ]

        colWidths = [
            0.8 * inch,
            1.0 * inch,
            0.8 * inch,
            2.8 * inch,
            1.0 * inch,
            1.0 * inch,
        ]

        summary_table = Table(summary_data, colWidths=colWidths)

        # Style the summary table
        summary_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, -3), (-1, -1), "CENTER"),
                    (
                        "GRID",
                        (0, -3),
                        (6, -3),
                        1,
                        colors.black,
                    ),  # Grid for the last rows
                    (
                        "GRID",
                        (5, -2),
                        (6, -1),
                        1,
                        colors.black,
                    ),  # Grid for the last rows'
                    ("SPAN", (0, -3), (1, -3)),
                ]
            )
        )

        # Add summary table wrapped in KeepTogether to prevent splitting
        elements.append(KeepTogether(summary_table))

        # Build the PDF
        pdf.build(elements)
        print(f"Invoice generated: {filename}")

    def delete_invoice(self, filename):
        """Delete the PDF invoice"""
        try:
            os.remove(filename)
            print(f"Invoice deleted: {filename}")
        except FileNotFoundError:
            print(f"Error: File not found at path: {filename}")

    def create_pdf_data(self, orders_without_pdf, sellercloud_orders, spinner: Spinner):
        """Parse the data to be used in the invoice"""
        spinner.start("Creating PDF data...")
        all_data = []
        for po_reference, reference_data in orders_without_pdf.items():
            sellercloud_data = {
                item["ProductIDOriginal"]: {
                    "description": item["ProductName"],
                    "unit_price": item["PricePerCase"],
                    "line_total": item["LineTotal"],
                }
                for item in sellercloud_orders[po_reference]["Items"]
            }
            items, subtotal = self._create_items(
                sellercloud_data, reference_data["pos"]
            )
            invoice_data = {
                "reference": self._convert_string_safe(po_reference),
                "date": reference_data["prod_date"],
                "items": items,
                "subtotal": subtotal,
                "fees": 0.00,
                "total": subtotal,
            }

            all_data.append(invoice_data)

        spinner.stop()
        return all_data

    def _create_items(self, sellercloud_data, parts):
        items = []
        subtotal = 0.00
        for part in parts:
            item = {
                "po": part["po_number"],
                "part": part["rc_part"],
                "qty": part["qty"],
                "description": sellercloud_data[part["rc_part"]]["description"],
                "unit_price": sellercloud_data[part["rc_part"]]["unit_price"],
                "line_total": sellercloud_data[part["rc_part"]]["line_total"],
            }
            subtotal += item["line_total"]
            items.append(item)

        return items, subtotal

    def _convert_string_safe(self, input_str):
        # Use regular expression to keep only letters and numbers
        return re.sub(r"[^A-Za-z0-9]", "", input_str)


# Example usage -----------------------------------------------------------------------------------------------------------

# invoice_data = {
#     "reference": "TTTTTTT",
#     "date": "5/17/2023",
#     "items": [
#         {
#             "po": "67648",
#             "part": "RD2-68018",
#             "qty": 40,
#             "description": "Here is the description of the part",
#             "unit_price": 52.99,
#             "line_total": 2119.60,
#         },
#         {
#             "po": "68018",
#             "part": "RD2-68019",
#             "qty": 50,
#             "description": "Here is the description of the part",
#             "unit_price": 52.99,
#             "line_total": 2649.50,
#         },
#         # Add more items...
#     ],
#     "subtotal": 43087.95,
#     "fees": 0.00,
#     "total": 43087.95,
# }


# invoice = InvoiceGenerator(logo_path="logo.png")
# invoice.generate_invoice(invoice_data, "invoice.pdf")
