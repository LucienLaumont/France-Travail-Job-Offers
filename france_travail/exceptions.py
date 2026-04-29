class FranceTravailError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(FranceTravailError):
    pass


class RateLimitError(FranceTravailError):
    pass


class BadRequestError(FranceTravailError):
    pass


class ServerError(FranceTravailError):
    pass
