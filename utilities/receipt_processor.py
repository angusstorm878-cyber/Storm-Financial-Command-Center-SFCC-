from datetime import datetime


def process_receipt_text(receipt_text):

    """
    Converts OCR receipt text into transaction data
    """

    transaction = {

        "date": datetime.now().strftime("%Y-%m-%d"),

        "description": extract_description(
            receipt_text
        ),

        "category": extract_category(
            receipt_text
        ),

        "amount": extract_amount(
            receipt_text
        ),

        "type": "Expense"

    }


    return transaction





def extract_description(text):

    lines = text.split("\n")

    if lines:

        return lines[0]

    return "Receipt Purchase"





def extract_category(text):

    text = text.lower()


    if "walmart" in text or "target" in text:

        return "Groceries"


    if "gas" in text or "fuel" in text:

        return "Fuel"


    if "restaurant" in text or "food" in text:

        return "Dining"


    return "Other"





def extract_amount(text):

    import re


    amounts = re.findall(
        r"\d+\.\d{2}",
        text
    )


    if amounts:

        return float(
            amounts[-1]
        )


    return 0.0