from model.virtual_machine import VirtualMachine
from presenter.simplestudio_presenter import SimpleStudioPresenter
from view.main_view import SimpleStudioViewInterface

def main():
    virtual_machine = VirtualMachine()    
    simplestudio_presenter = SimpleStudioPresenter(virtual_machine) 
    simplestudio_view = SimpleStudioViewInterface(simplestudio_presenter)
    simplestudio_presenter.set_view(simplestudio_view)
    simplestudio_presenter.start()

if __name__ == "__main__":
    main()
