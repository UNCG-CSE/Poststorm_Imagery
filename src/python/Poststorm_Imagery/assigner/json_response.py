import jsonpickle


class JSONResponse:
    """
    A class that simply contains only important values and functions to quickly convert Python data into a response
    for communicating with languages that can parse JSON-objects. This class uses the jsonpickle library to serialize
    most Python objects into JSON if they are passed into any of the fields. Objects are stored without their object
    information, so it is highly recommended not to use this class to serialize data for de-serialization in Python
    later, but instead to permanently serialize data for anything other than Python use.
    """

    status: int = -1  # -1 = pre-mature termination, 0 = successful, 1 = error
    content: str  # The intended content
    error_message: str  # What went wrong

    def __init__(self, status: int, content=None, error_message: str = None):
        self.status = status
        if self.status is 0:
            self.content = content
        elif self.status is 1:
            self.error_message = error_message
        else:
            self.status = 1
            if error_message is None or len(error_message) is 0:
                self.error_message = 'Unknown error in json response object input'
            else:
                self.error_message = error_message

    def json(self):
        return jsonpickle.encode(self, unpicklable=False)
