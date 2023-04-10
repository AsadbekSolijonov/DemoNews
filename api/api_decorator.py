def try_except(function):
    """
    This is a Decorator
    Goal: Returns the result if API keys exist, otherwise None.
    """

    def wrapper(*args, **kwargs):
        """
        This decorator prevents the program
        from crashing if some fields are invalid keys.
        """
        try:
            result = function(*args, **kwargs)
            return result
        except KeyError as e:
            return

    return wrapper
