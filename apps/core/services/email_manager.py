import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pytest_is_running import is_running

from apps.accounts.services.token import TokenService
from config.settings import EmailServiceConfig, AppConfig


class EmailService:
    config = EmailServiceConfig.get_config()
    app = AppConfig.get_config()

    @classmethod
    def __send_email(cls, subject: str, body: str, to_address: str):
        try:
            message = MIMEMultipart()
            message['From'] = 'Daniil <support@daniilithub.ru>'
            message['To'] = to_address
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP(cls.config.smtp_server, cls.config.smtp_port) as server:
                # server.set_debuglevel(1)
                server.login(cls.config.smtp_username, cls.config.smtp_password)
                server.sendmail('Daniil <support@daniilithub.ru>', to_address, message.as_string())
                server.quit()
        except Exception as e:
            print(f"An error occurred while sending email: {e}")

    @classmethod
    def __print_test_otp(cls, otp: str):
        dev_show = f"--- Testing OTP: {otp} ---"
        print(dev_show)

    @classmethod
    def __send_verification_email(cls, subject, body, to_address):
        """
        Sends a verification email or prints OTP in testing mode.
        """

        if is_running() or cls.config.use_local_fallback:
            cls.__print_test_otp(TokenService.create_otp_token())
        else:
            cls.__send_email(subject, body, to_address)

    @classmethod
    def register_send_verification_email(cls, to_address):
        """
        Sends a verification email for the registration process.
        """

        otp = TokenService.create_otp_token()
        subject = 'Проверка электронной почты'
        body = f"Спасибо, что зарегистрировались в {cls.app.app_name}!\n\n" \
               f"Чтобы завершить регистрацию, введите следующий код: {otp}\n\n" \
               f"Если вы не зарегистрировались, проигнорируйте это письмо."
        cls.__send_verification_email(subject, body, to_address)

    @classmethod
    def reset_password_send_verification_email(cls, to_address):
        """
        Sends a verification email for the password reset process.
        """

        otp = TokenService.create_otp_token()
        subject = 'Подтверждение сброса пароля'
        body = f"Мы получили запрос на сброс вашего {cls.app.app_name} пароля.\n\n" \
               f"Пожалуйста, введите следующий код, чтобы сбросить пароль: {otp}\n\n" \
               f"Если вы не запрашивали это, можете проигнорировать это письмо."
        cls.__send_verification_email(subject, body, to_address)

    @classmethod
    def change_email_send_verification_email(cls, new_email: str):
        """
        Sends a verification email for the email change process.
        """

        otp = TokenService.create_otp_token()
        subject = 'Проверка изменения электронной почты'
        body = f"Мы получили запрос на изменение электронной почты, связанной с вашим {cls.app.app_name} аккаунтом.\n\n" \
               f"Чтобы подтвердить это изменение, введите следующий код: {otp}\n\n" \
               f"Если вы не запрашивали это, обратитесь в нашу службу поддержки."
        cls.__send_verification_email(subject, body, new_email)
