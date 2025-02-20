import pyodbc
from config import create_connection_string, db_config
from datetime import datetime
from spinner import Spinner


class ExampleDb:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(create_connection_string(db_config["ExampleDb"]))
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            print(f"Error establishing connection to the ExampleDb database: {e}")
            raise

    def get_orders_without_pdf(self, spinner: Spinner):
        """Gets the orders from the database that need to be created in SellerCloud."""
        try:
            spinner.start("Getting orders without PDF invoices...")
            self.cursor.execute(
                """
                SELECT * FROM ProductionOrders WHERE pdf_invoiced = 0 AND in_sellercloud = 1
                """
            )

            orders = {}

            for row in self.cursor.fetchall():
                po_number = row.po_number.strip()
                po_reference = row.ref_number.strip()
                prod_date = row.prod_date.strftime("%m/%d/%Y")

                if po_reference not in orders:
                    orders[po_reference] = {
                        "prod_date": prod_date,
                        "pos": [
                            {
                                "po_number": po_number,
                                "rc_part": row.rc_part,
                                "alias_part": row.alias_part,
                                "qty": row.qty,
                            }
                        ],
                    }
                else:
                    orders[po_reference]["pos"].append(
                        {
                            "po_number": po_number,
                            "rc_part": row.rc_part,
                            "alias_part": row.alias_part,
                            "qty": row.qty,
                        }
                    )

        except Exception as e:
            spinner.stop()
            print(f"Error while checking for duplicate: {e}")
            raise

        ref_numbers = list(orders.keys())
        spinner.stop()
        return orders, ref_numbers

    def update_status(self, ref_number):
        """Updates the order in the database."""
        try:
            self.cursor.execute(
                """
                UPDATE ProductionOrders SET
                    pdf_invoiced = 1, 
                    pdf_invoiced_date = ?
                WHERE ref_number = ?
                """,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ref_number,
            )

            self.conn.commit()

        except Exception as e:
            print(f"Error while updating orders: {e}")
            raise

    def close(self):
        self.cursor.close()
        self.conn.close()
