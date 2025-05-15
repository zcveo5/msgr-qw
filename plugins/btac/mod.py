#Start

app = None
class AuthPlugin:
    @staticmethod
    def give_data(v):
        global app
        app = v

    @staticmethod
    def execute():
        pass
#End