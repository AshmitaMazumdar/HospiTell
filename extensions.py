from flask_mail import Mail
import logging

logger = logging.getLogger(__name__)


class SafeMail(Mail):
    """
    Safe wrapper around Flask-Mail.
    Logs an error and shows a visible user flash notice instead of raising
    an unhandled exception if SMTP credentials are missing, revoked, or unreachable.
    """
    def send(self, message):
        try:
            super().send(message)
            return True
        except Exception as e:
            logger.error(f"Email send failed: {type(e).__name__} - {e}", exc_info=True)
            try:
                from flask import flash, has_request_context
                if has_request_context():
                    flash("Notice: Email notification could not be sent (SMTP server unavailable).", "warning")
            except Exception:
                pass
            return False

    def send_message(self, *args, **kwargs):
        try:
            super().send_message(*args, **kwargs)
            return True
        except Exception as e:
            logger.error(f"Email send_message failed: {type(e).__name__} - {e}", exc_info=True)
            try:
                from flask import flash, has_request_context
                if has_request_context():
                    flash("Notice: Email notification could not be sent (SMTP server unavailable).", "warning")
            except Exception:
                pass
            return False


mail = SafeMail()
