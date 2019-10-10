import jsonpickle


class JSONResponse:

    status: int = -1  # -1 = pre-mature termination, 0 = successful, 1 = error
    content: str  # The intended content
    error_message: str  # What went wrong

    def __init__(self, status: int, content: str = None, error_message: str = None):
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
