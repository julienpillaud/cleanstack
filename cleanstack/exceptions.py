class DomainError(Exception):
    pass


class BadRequestError(DomainError):
    pass


class ForbiddenError(DomainError):
    pass


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class UnprocessableEntityError(DomainError):
    pass
