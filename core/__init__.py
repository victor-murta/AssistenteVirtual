import datetime


class Systeminfo:
    def __init__(self):
        pass

    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        answer = f'São {now.hour} e {now.minute} minutos'
        return answer

