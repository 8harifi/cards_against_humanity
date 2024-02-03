class RoomAuthError(Exception):
    def __init__(self, message: str = None):
        """

        :param message:
        """
        self.message = message
        super().__init__(message)


class UserAuthError(Exception):
    def __init__(self, message: str = None):
        """

        :param message:
        """
        self.message = message
        super().__init__(message)
