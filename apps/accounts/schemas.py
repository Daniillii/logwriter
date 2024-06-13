from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from apps.accounts.services.password import PasswordManager


class ValidatePasswordInSchema(BaseModel):
    password: str
    password_confirm: str

    @field_validator("password")
    def validate_password(cls, password: str):
        return PasswordManager.validate_password_strength(password=password, has_special_char=False)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Пароли не совпадают!')
        return self


# ------------------------
# --- Register Schemas ---
# ------------------------

class RegisterIn(ValidatePasswordInSchema):
    email: EmailStr

    @staticmethod
    def examples():
        examples = {
            'openapi_examples': {
                "default": {
                    "summary": "Default",
                    "value": {
                        "email": "user@example.com",
                        "password": "string",
                        "password_confirm": "string"
                    },
                },
                "with-email": {
                    "summary": "Регистрация нового пользователя с проверкой по электронной почте (OTP)",
                    "description": """

> `email: "user@example.com"` Уникальный адрес электронной почты пользователя. Попытка присвоить пользователям один и тот же адрес электронной почты
возвращает ошибку.
> 
> ``password:"<Password1>"` Пароль.
> 
> ``password:"<Password1>"` Пароль, который подтвержден.  
    
Для правильного пароля необходимо:
* Использовать в пароле цифры _**0-9**_.
* Использовать строчные символы _**a-z**_ в пароле.
* Использовать в пароле символы верхнего регистра _**A-Z**_.
* **Опционально:** Использовать в пароле специальные символы __!?@#$%^&*()+{}[]<>/__.""",
                    "value": {
                        "email": "user@example.com",
                        "password": "NewPassword123",
                        "password_confirm": "NewPassword123"
                    },
                }
            }
        }
        return examples


class RegisterOut(BaseModel):
    email: EmailStr
    message: str


class RegisterVerifyIn(BaseModel):
    email: EmailStr
    otp: str


class RegisterVerifyOut(BaseModel):
    access_token: str
    message: str


# --------------------
# --- Login Schemas ---
# --------------------
class LoginOut(BaseModel):
    access_token: str
    token_type: str


# ------------------------
# --- Password Schemas ---
# ------------------------

class PasswordResetIn(BaseModel):
    email: EmailStr


class PasswordResetOut(BaseModel):
    message: str


class PasswordResetVerifyIn(ValidatePasswordInSchema):
    email: EmailStr
    otp: str


class PasswordResetVerifyOut(BaseModel):
    message: str


class PasswordChangeIn(ValidatePasswordInSchema):
    current_password: str

    @staticmethod
    def examples():
        examples = {
            'openapi_examples': {
                "valid": {
                    "summary": "Действительный пароль",
                    "description": """Для правильного пароля необходимо:
* Использовать в пароле цифры _**0-9**_.
* Использовать в пароле строчные символы _**a-z**_.
* Использовать в пароле символы верхнего регистра _**A-Z**_.
* **Опционально:** Использовать в пароле специальные символы __!?@#$%^&*()+{}[]<>/__.
                        """,
                    "value": {
                        "current_password": "Password123!",
                        "password": "NewPassword123!",
                        "password_confirm": "NewPassword123!"
                    },
                }
            }}
        return examples


class PasswordChangeOut(BaseModel):
    message: str


# -------------------
# --- OTP Schemas ---
# -------------------

class OTPResendIn(BaseModel):
    request_type: str
    email: EmailStr

    @field_validator("request_type")
    def validate_request_type(cls, value):
        allowed_request_types = {"register", "reset-password", "change-email"}
        if value not in allowed_request_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный тип запроса. Допустимые значения: 'register', 'reset-password', 'change-email'.")
        return value

    @staticmethod
    def examples():
        examples = {
            'openapi_examples': {
                "default": {
                    "summary": "По умолчанию",
                    "description": """
- `Тип_запроса`: Определяет цель запроса OTP. Допустимые значения: "регистрация", "сброс пароля", 
  или "change-email".
- `email`: Основной адрес электронной почты пользователя.
""",
                    "value": {
                        "request_type": "string",
                        "email": "user@example.com"
                    },
                },
                "register": {
                    "summary": "Повторная отправка OTP для регистрации пользователя",
                    "value": {
                        "request_type": "register",
                        "email": "user@example.com"
                    },
                },
                "reset-password": {
                    "summary": "Повторная отправка OTP для сброса пароля",
                    "value": {
                        "request_type": "reset-password",
                        "email": "user@example.com"
                    },
                },
                "change-email": {
                    "summary": "Повторная отправка OTP для изменения электронной почты",
                    "value": {
                        "request_type": "change-email",
                        "email": "user@example.com"
                    },
                },
            }
        }
        return examples


# ----------------------------
# --- Change-Email Schemas ---
# ----------------------------

class EmailChangeIn(BaseModel):
    new_email: EmailStr


class EmailChangeOut(BaseModel):
    message: str


class EmailChangeVerifyIn(BaseModel):
    otp: str


class EmailChangeVerifyOut(BaseModel):
    message: str


# --------------------
# --- User Schemas ---
# --------------------


class UserSchema(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    is_verified_email: bool
    date_joined: str
    updated_at: str
    last_login: str


class CurrentUserOut(BaseModel):
    user: UserSchema


class UpdateUserSchema(BaseModel):
    first_name: str | None
    last_name: str | None


class UpdateUserIn(BaseModel):
    user: UpdateUserSchema
