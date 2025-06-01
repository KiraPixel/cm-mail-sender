from sqlalchemy import select

from html import prepare_content_by_template
from .models import Mailing
from . import get_db_session, SessionLocal


class MailingMessage:
    def __init__(self, message_id: int, db_session):
        self.db_session = db_session
        self.message = db_session.get(Mailing, message_id)
        if not self.message:
            raise ValueError(f"Message with id {message_id} not found")

        if self.message.html_template:
            processed_content  = prepare_content_by_template(self.message.html_template, self.message.content)
            if processed_content is None:
                self.set_new_status('template_error')
            else:
                self.message.content = processed_content
                self.db_session.commit()

    def set_new_status(self, new_status: str):
        self.message.status = new_status
        self.db_session.commit()

    def set_time_sent_at(self, timestamp: int):
        self.message.sent_at = timestamp
        self.db_session.commit()

    def delete_attachment_content(self):
        self.message.attachment_content = b"sended"
        self.db_session.commit()

    def delete_html_content(self):
        self.message.content = b"html_content"
        self.db_session.commit()


def get_new_messages(db_session=None):
    session = db_session or SessionLocal()

    try:
        stmt = select(Mailing).where(Mailing.status == 'new')
        new_messages = session.execute(stmt).scalars().all()
        if not new_messages:
            return None
        return [MailingMessage(message.id, session) for message in new_messages]
    except Exception as e:
        print(e)
        return None
