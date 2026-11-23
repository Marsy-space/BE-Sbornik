import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_USER = "твой_логин_mailtrap"

def send_verification_email(to_email: str, token: str):
    # Ссылка туда, где будет обрабатываться токен
    verify_link = f"http://localhost:5173/src/pages/verify-email.html?token={token}"

    # Для учебного проекта пока выводим ссылку в консоль
    print(f"\n[EMAIL] Ссылка для подтверждения: {verify_link}\n")

    # Реальная отправка (закомментирована, чтобы не было ошибок)
    """
    msg = MIMEText(f"Пожалуйста, подтвердите ваш email, перейдя по ссылке: {verify_link}")
    msg['Subject'] = "Подтверждение Email - Сборник Рецептов"
    msg['From'] = "noreply@recipes.com"
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, "твой_пароль_mailtrap")
            server.send_message(msg)
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")
    """