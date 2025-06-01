import time
from db.messages import get_new_messages
from modules.api_cm import get_cm_health
from modules.mail_sender import send_email


def start_processing():
    new_messages = get_new_messages()
    if not get_cm_health():
        print("Приложите подорожник к ЦМ")
        print("Фрижу процесс на 1 минуту")
        time.sleep(60)
        return
    if new_messages:
        for message_obj in new_messages:
            print(f'try send message to {message_obj.message.target_email}')
            if message_obj.message.status != 'new':
                pass
            send_mail=send_email(message_obj.message.target_email, message_obj.message.subject, message_obj.message.content, attachment_name=message_obj.message.attachment_name, attachment_content=message_obj.message.attachment_content)
            if send_mail:
                message_obj.set_new_status('sent')
                message_obj.set_time_sent_at(time.time())
                if message_obj.message.attachment:
                    message_obj.delete_attachment_content()
                if message_obj.message.html_template is not None:
                    message_obj.delete_html_content()
            else:
                message_obj.set_new_status('error')
                if message_obj.message.attachment:
                    message_obj.delete_attachment_content()


if __name__ == "__main__":
    print("Запуск mail sender...")
    while True:
        start_processing()
        time.sleep(10)