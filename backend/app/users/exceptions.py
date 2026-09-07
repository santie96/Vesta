from app.core.exceptions.exceptions import (
    AlreadyExistsException, 
    NotFoundException, 
    ValidationException
)


class UserNotFoundException(NotFoundException):
    pass


class UserAlreadyExistsException(AlreadyExistsException):
    pass


class UserValidationException(ValidationException):
    pass