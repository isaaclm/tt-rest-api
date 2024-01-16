class TokenGenerationError(Exception):
    """
    Exception raised when there is an error during token generation.

    This exception is intended to be raised when there's an issue while generating
    an authentication token for a specific operation. It provides a way to handle
    token-related errors in a more organized manner.

    Attributes:
        response (requests.response): The response from the unsuccessful request to get a token.
    """

    def __init__(self, response):
        error_message = "Token acquisition failed"
        try:
            error_data = response.json()  # If the response contains error details
            error_message += "\nStatus Code: {}".format(error_data.get("statusCode", "unknown"))
            error_message += "\nStatus Description: {}".format(error_data.get("status_desc", "none"))
        except ValueError:
            pass  # Response wasn't JSON or didn't contain error details

        super().__init__(error_message)


class NotAuthorisedError(Exception):
    """
    Exception raised when there hasn't been a successful authorisation call to get token.
    """

    def __init__(self):
        error_message = "You attempted to make a call to the TT REST API 2.0 without an authorised token."
        super().__init__(error_message)


class PostRequestError(Exception):
    """
    Exception raised when there has been an error with a POST request
    """

    def __init__(self, response):
        error_message = "POST request error"
        self.response = response

        try:
            error_data = response.json()  # If the response contains error details
            error_message += "\nStatus Code: {}".format(error_data.get("error_message", error_message))
            error_message += "\nError Message: {}".format(error_data.get("error_message", error_message))
            error_message += "\nText: {}".format(error_data.get("text", error_message))
        except ValueError:
            pass  # Response wasn't JSON or didn't contain error details

        super().__init__(error_message)


class UsageError(Exception):
    """
    Exception raised when an API call has been requested with invalid arguments.
    """

    def __init__(self, error_message):
        super().__init__(error_message)
