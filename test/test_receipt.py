import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


from database import (
    initialize_database,
    add_receipt,
    get_receipts,
    delete_receipt
)


def test_receipt_flow():

    initialize_database()


    add_receipt(
        1,
        "Walmart",
        54.73,
        "receipts/test.png",
        "Groceries"
    )


    receipts = get_receipts()


    assert len(receipts) > 0


    receipt_id = receipts[0][0]


    delete_receipt(
        receipt_id
    )


    print(
        "Receipt CRUD test passed"
    )



if __name__ == "__main__":

    test_receipt_flow()