import os
from exchangelib import Credentials, Account, Message, DELEGATE, HTMLBody, FileAttachment, Configuration

sender_email = os.getenv('MAIL_MAIL', 'nomail@nomail')
sender_user = os.getenv('MAIL_USERNAME', 'user')
sender_domain = os.getenv('MAIL_USERNAME_DOMAIN', 'mail')
sender_password = os.getenv('MAIL_PASSWORD', 'password')
sender_host = os.getenv('MAIL_HOST', 'mail.ru')
use_domain_format = os.getenv('USE_DOMAIN_FORMAT', 'at')
full_username = ''

if use_domain_format == 'backslash':
    full_username = f"{sender_domain}\\{sender_user}"
else:
    full_username = f"{sender_user}@{sender_domain}"

def send_email(target_email, subject, body, attachment_name=None, attachment_content=None):
    try:
        config = Configuration(
            server=sender_host,
            credentials=Credentials(username=full_username, password=sender_password)
        )

        account = Account(sender_email, config=config, autodiscover=False, access_type=DELEGATE)

        msg = Message(
            account=account,
            folder=account.sent,
            subject=subject,
            body=HTMLBody(body),
            to_recipients=[target_email]
        )
        print(f'Send email to {target_email} with subject "{subject}" from "{sender_email}" login {full_username}')
        if attachment_name:
            attachment = FileAttachment(
                name=attachment_name,
                content=attachment_content,
            )
            msg.attach(attachment)

        msg.send()
        return True
    except Exception as e:
        print(f'Произошла ошибка при отправке сообщения: {e}')
        return False


