from pydantic import BaseModel, ConfigDict, EmailStr


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "ivanov@gmail.com",
                "password": "123"
            }
        }
    )
