import logging
from typing import Any

from jinja2 import Environment, FileSystemLoader
import os

# Определяем путь к папке шаблонов
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "standalone")
logger = logging.getLogger('cm_mail_sender')

# Инициализация Jinja2 окружения
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def process_html_template(html_template: str, content: dict) -> str:
    """
    Обрабатывает шаблон HTML и возвращает сгенерированное содержимое.

    :param html_template: Название шаблона, например 'new_password' или 'new_user'.
    :param content: Словарь с данными для рендера шаблона.
    :return: Сгенерированное содержимое HTML.
    """
    try:
        template = env.get_template(f"{html_template}.html")
        return template.render(content)
    except Exception as e:
        logger.error(f"Ошибка обработки шаблона {html_template}: {e}")
        return None


def prepare_content_by_template(template_name: str, content):
    """
    Формирует данные для шаблона на основе его типа.

    :param template_name: Название шаблона, например 'new_password' или 'new_user'.
    :param message_obj: Объект сообщения с данными.
    :return: Вернем html страницу
    """
    if template_name is None or content is None:
        return None

    if template_name == "new_password":
        data = {"password": content}
        return process_html_template(template_name, data)
    elif template_name == "new_user":
        try:
            username, password = content.split('|')
        except ValueError:
            return None
        data = {
            "username": username,
            "password": password,
        }
        return process_html_template(template_name, data)
    else:
        logger.error(f"Неизвестный шаблон {template_name}:")
        return None
