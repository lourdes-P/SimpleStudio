
from CTkMessagebox import CTkMessagebox

class CustomDialog:
    
    @staticmethod
    def display_yes_no(master, message, title = "Continue?"):
        yes_no_response = CTkMessagebox(
            title=title,
            message=message,
            icon="question",
            option_1="Yes",
            option_2="No",
            width= 300,
            height= 200,
            master=master
        )
        return yes_no_response.get()
    
    @staticmethod
    def display_error(master, message):
        CTkMessagebox(
            title="ERROR",
            message=message,
            icon="cancel",
            option_1="OK",
            width= 300,
            height= 200,
            master=master
        )