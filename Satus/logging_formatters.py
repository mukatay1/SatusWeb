from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = record.asctime
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        if not log_record.get('module'):
            log_record['module'] = record.module
        if not log_record.get('name'):
            log_record['name'] = record.name
        if not log_record.get('level'):
            log_record['level'] = record.levelname
