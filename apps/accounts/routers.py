from fastapi import APIRouter, status, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from apps.accounts import schemas
from apps.accounts.services.authenticate import AccountService
from apps.accounts.services.permissions import Permission
from apps.accounts.services.user import User, UserManager

router = APIRouter(
    prefix='/accounts'
)


# ------------------------
# --- Register Routers ---
# ------------------------


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.RegisterOut,
    summary='Регистрация нового пользователя',
    description="""## Зарегистрируйте нового пользователя по электронной почте и паролю, а затем отправьте OTP-код на его электронный адрес.
    
Генерирует код активации учетной записи для пользователя, чья учетная запись еще не включена.

Код активации учетной записи, сгенерированный этой конечной точкой, предназначен для одноразового использования и истекает через 5 минут. 
Если к этой конечной точке будет сделан новый POST-запрос, то будет сгенерирован новый код, если срок действия предыдущего кода истек. Новый
 сгенерированный код будет действовать еще 5 минут, в то время как предыдущий код уже не будет действителен.

После запроса на регистрацию эта конечная точка отправит OTP-код на адрес электронной почты пользователя. Необходимо 
проверить этот OTP-код с помощью конечной точки `/accounts/register/verify`. Проверка подтверждает адрес электронной почты пользователя и 
активирует учетную запись.
 
Обратите внимание, что пользователи не смогут войти в свои учетные записи до тех пор, пока их адреса электронной почты не будут подтверждены.
""",
    tags=['Авторизация'])
async def register(payload: schemas.RegisterIn = Body(**schemas.RegisterIn.examples())):
    return AccountService.register(**payload.model_dump(exclude={"password_confirm"}))


@router.patch(
    '/register/verify',
    status_code=status.HTTP_200_OK,
    response_model=schemas.RegisterVerifyOut,
    summary='Проверка регистрации пользователей',
    description='Проверьте регистрацию нового пользователя, подтвердив предоставленный OTP.',
    tags=['Авторизация'])
async def verify_registration(payload: schemas.RegisterVerifyIn):
    return AccountService.verify_registration(**payload.model_dump())


# ---------------------
# --- Login Routers ---
# ---------------------


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=schemas.LoginOut,
    summary='Вход в систему для пользователя',
    description='Вход в систему пользователя с действительными учетными данными, если учетная запись пользователя активна.',
    tags=['Авторизация'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return AccountService.login(form_data.username, form_data.password)


@router.post(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Выход пользователя из системы',
    description="Выход из системы текущего аутентифицированного пользователя. "
                "Отзывает маркер доступа пользователя и аннулирует сессию.",
    tags=['Авторизация'])
async def logout(current_user: User = Depends(AccountService.current_user)):
    AccountService.logout(current_user)


# ------------------------
# --- Password Routers ---
# ------------------------


@router.post(
    '/reset-password',
    status_code=status.HTTP_200_OK,
    response_model=schemas.PasswordResetOut,
    summary='Сброс пароля',
    description="Инициируйте запрос на сброс пароля, отправив письмо с подтверждением на пользовательский адрес "
                "зарегистрированный адрес электронной почты.",
    tags=['Авторизация'])
async def reset_password(payload: schemas.PasswordResetIn):
    return AccountService.reset_password(**payload.model_dump())


@router.patch(
    '/reset-password/verify',
    status_code=status.HTTP_200_OK,
    response_model=schemas.PasswordResetVerifyOut,
    summary='Проверка сброса пароля',
    description="Проверьте запрос на сброс пароля, подтвердив предоставленный OTP, отправленный на пользовательский номер "
                "зарегистрированный адрес электронной почты. Если изменение прошло успешно, пользователю нужно будет снова войти в систему.",
    tags=['Авторизация'])
async def verify_reset_password(payload: schemas.PasswordResetVerifyIn):
    return AccountService.verify_reset_password(**payload.model_dump(exclude={"password_confirm"}))


# -------------------
# --- OTP Routers ---
# -------------------


@router.post(
    '/otp',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Повторная отправка OTP',
    description="""Позволяет пользователю запросить новый пароль OTP (One-Time Password) для регистрации, сброса пароля,
    или проверки изменения электронной почты.

### Рекомендации по использованию:
- Для **регистрации** и **сброса пароля** укажите **основной адрес электронной почты** пользователя.
- Для **изменения электронной почты** также укажите **основной адрес электронной почты** (а не новый непроверенный адрес).
    """,

    tags=['Авторизация'])
async def resend_otp(payload: schemas.OTPResendIn = Body(**schemas.OTPResendIn.examples())):
    AccountService.resend_otp(**payload.model_dump())


# ---------------------
# --- Users Routers ---
# ---------------------


@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=schemas.CurrentUserOut,
    summary='Получение текущего пользователя',
    description='Получение текущего пользователя, если он активен.',
    tags=['Пользователи'])
async def retrieve_me(current_user: User = Depends(AccountService.current_user)):
    return {'user': UserManager.to_dict(current_user)}


@router.put(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=schemas.CurrentUserOut,
    summary='Обновление текущего пользователя',
    description='Обновление текущего пользователя.',
    tags=['Пользователи'])
async def update_me(payload: schemas.UpdateUserSchema, current_user: User = Depends(AccountService.current_user)):
    user = UserManager.update_user(current_user.id, **payload.model_dump())
    return {'user': UserManager.to_dict(user)}


@router.patch(
    '/me/password',
    status_code=status.HTTP_200_OK,
    response_model=schemas.PasswordChangeOut,
    summary='Изменение пароля текущего пользователя',
    description='Изменение пароля для текущего пользователя. Если изменение прошло успешно, пользователь '
                'нужно снова войти в систему.',
    tags=['Пользователи'])
async def change_password(payload: schemas.PasswordChangeIn = Body(**schemas.PasswordChangeIn.examples()),
                          current_user: User = Depends(AccountService.current_user)):
    return AccountService.change_password(current_user, **payload.model_dump(exclude={"password_confirm"}))


@router.post(
    '/me/email',
    status_code=status.HTTP_200_OK,
    response_model=schemas.EmailChangeOut,
    summary='Изменение текущего пользователя email',
    description="""## Измените адрес электронной почты для текущего пользователя.

После установки нового адреса электронной почты на него будет отправлен OTP-код для проверки.
""",
    tags=['Пользователи'])
async def change_email(email: schemas.EmailChangeIn, current_user: User = Depends(AccountService.current_user)):
    return AccountService.change_email(current_user, **email.model_dump())


@router.patch(
    '/me/email/verify',
    status_code=status.HTTP_200_OK,
    response_model=schemas.EmailChangeVerifyOut,
    summary='Проверка изменения электронной почты текущего пользователя',
    description="""## Проверка изменения адреса электронной почты текущего пользователя.

Проверка кода OTP, отправленного на новый адрес электронной почты пользователя. Если OTP действителен, новый
адрес электронной почты будет сохранен в качестве основного адреса электронной почты пользователя.
""",
    tags=['Пользователи'])
async def verify_change_email(otp: schemas.EmailChangeVerifyIn,
                              current_user: User = Depends(AccountService.current_user)):
    return AccountService.verify_change_email(current_user, **otp.model_dump())


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.CurrentUserOut,
    summary='Получение одного пользователя',
    description='Получение одного пользователя по идентификатору. Только администраторы могут читать данные пользователей.',
    tags=['Пользователи'],
    dependencies=[Depends(Permission.is_admin)]
)
async def retrieve_user(user_id: int):
    return {'user': UserManager.to_dict(UserManager.get_user(user_id))}

# TODO DELETE /accounts/me
# TODO add docs and examples to endpoints
