from model.virtual_machine import VirtualMachine
from presenter.simplestudio_presenter import SimpleStudioPresenter

def main():
    virtual_machine = VirtualMachine()    
    simplestudio_presenter = SimpleStudioPresenter(virtual_machine) 
    simplestudio_presenter.start()

if __name__ == "__main__":
    main()
