class RepositoryError(Exception):
    pass


class InvalidFieldError(RepositoryError):
    pass


class InvalidFilterError(RepositoryError):
    pass


ERROR_MAPPING: dict[type[RepositoryError], int] = {
    InvalidFieldError: 422,
    InvalidFilterError: 422,
}


def get_status_error(exc: RepositoryError) -> int:
    status_code = 500

    for error_cls in type(exc).mro():
        if issubclass(error_cls, RepositoryError) and error_cls in ERROR_MAPPING:
            status_code = ERROR_MAPPING[error_cls]
            break

    return status_code
