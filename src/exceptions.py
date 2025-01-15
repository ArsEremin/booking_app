from fastapi import HTTPException, status

UserExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="user already exists"
)

InvalidAuthDataException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid email or password"
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="token expired"
)
