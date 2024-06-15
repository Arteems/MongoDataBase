from fastapi import HTTPException, status


class UserNotFoundHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )


class UsernameAllreadyExistHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="username allready exist",
        )
