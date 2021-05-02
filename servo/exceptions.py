class SerialConnectionError(BaseException):
    """
    Exception rasied for errors in the Serial connection between ECU and Motor
    """
    def __init__(self, message="Either there is no serial connection between Motor and Controller Unit or there are driver problems"):
        self.message = message
        super().__init__(self.message)