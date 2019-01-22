def snake_to_camel(word):
    """
    changes word snake to camel case
    example: my_plan -> MyPlan
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def buildxml_string(url, kwargs):
    """
    This function creates xml payload using url &
    Keyword arguments
    """
    root = url.split('/')[-1]
    payload = ""
    if isinstance(kwargs, dict):
        for k, v in kwargs.items():
            k = snake_to_camel(k)
            if k[-2:] == "Id":
                k = k[:-2] + 'ID'
            payload += "<{}>{}</{}>".format(k, v, k)
    payload = "<" + root + ">" + payload + "</" + root + ">"
    return payload
