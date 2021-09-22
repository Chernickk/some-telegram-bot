import logging
import sys


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.user_id = record.args.get('user_id')
        return super().format(record)


message_handler = logging.StreamHandler(sys.stdout)
message_handler.setFormatter(CustomFormatter("%(levelname)-10s %(asctime)s message from %(user_id)s text: %(message)s"))


bot_message_logger = logging.getLogger('bot')
bot_message_logger.setLevel(logging.INFO)
bot_message_logger.addHandler(message_handler)

