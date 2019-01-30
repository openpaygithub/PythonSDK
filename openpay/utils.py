import datetime


def handle_response(root):
    """
    :param root: Root element of XML payload.
    :return: XML payload for Openpay API.
    """
    final_response = {}
    for value in root:
        if value.text is not None:
            final_response[value.tag] = value.text
    return final_response


def check_postal_code(postal_code):
    """
    :param postal_code: Postal code from Client.
    :return: Either exception for invalid postal code or return valid postal code.
    """
    if len(str(postal_code)) == 4:
        return postal_code
    raise TypeError("Postal code should be of length 4")


def check_date_format(date_val):
    """
    :param date_val: Date format validation.
    :return: Either exception for invalid date or return valid postal code.
    """
    if date_val:
        try:
            datetime.datetime.strptime(date_val, "%d %b %Y")
        except ValueError:
            raise ValueError("Invalid date format, it should be in 'dd-mm-yy'")
    return date_val
