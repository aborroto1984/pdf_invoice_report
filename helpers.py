from seller_cloud_api import SellerCloudAPI
from email_helper import send_email
from spinner import Spinner


class Helpers:
    def __init__(self):
        pass

    def batches_creator(self, objects, batch_size):
        """Creates batches of objects to be processed."""
        counter = 1
        container = []
        try:
            # It makes batches of 50 skus to send to SellerCloud
            while True:
                if len(objects) > batch_size:
                    batch = [objects.pop() for _ in range(batch_size)]
                else:
                    batch = objects
                    objects = []

                container.append(batch)

                if not objects:
                    print(f"Done creating batches of {batch_size}.")
                    return container

                counter += 1

        except Exception as e:
            print(f"Error creating batches: {e}")
            raise Exception(f"Error creating batches: {e}")

    def failure_reporting(self, where, sc_order_ids):
        string = "\n".join(sc_order_ids)
        send_email(f"Error {where}", f"Error {where} for SellerCloud ids: \n{string}.")

    def get_sellercloud_order(
        self, ref_numbers, sc_api: SellerCloudAPI, spinner: Spinner
    ):
        try:
            spinner.start("Getting SellerCloud order ids...")
            sellercloud_orders = {}
            for ref_number in ref_numbers:
                response = sc_api.execute(
                    {
                        "url_args": {
                            "ref_id": ref_number,
                        }
                    },
                    "GET_SELLERCLOUD_ORDER",
                )
                if response.status_code == 200:
                    sellercloud_orders[ref_number] = response.json()["Items"][0]
                else:
                    print(f"Error: Received status code {response.status_code}")
                    return None

            spinner.stop()
            return sellercloud_orders
        except Exception as e:
            spinner.stop()
            print(
                f"There was an error getting the sellercloud order id for PO: {ref_number}: {e}"
            )
            return None
