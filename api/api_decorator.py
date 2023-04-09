def try_except(function):
    """
    This is a Decorator
    Goal: Returns the result if API keys exist, otherwise None.
    """

    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
            return result
        except KeyError as e:
            return

    return wrapper
