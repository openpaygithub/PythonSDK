import datetime


def handle_response(root):
    final_response = {}
    for value in root:
        if value.text is not None:
            final_response[value.tag] = value.text
    return final_response


def check_postal_code(postal_code):
    if len(str(postal_code)) == 4:
        return postal_code
    raise TypeError("Postal code should be of length 4")


def check_date_format(date_val):
    if date_val:
        try:
            datetime.datetime.strptime(date_val, "%d %b %Y")
        except ValueError:
            raise ValueError("Invalid date format, it should be in 'dd-mm-yy'")
    return date_val
