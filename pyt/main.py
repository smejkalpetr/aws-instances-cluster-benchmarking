from src.controller import Controller

if __name__ == '__main__':
    ctrl = Controller()

    # for the assignment (everything automated)
    ctrl.initialize_env()
    ctrl.auto_setup()
    ctrl.auto_shutdown()

    # shows menu (used for testing purposes)
    # ctrl.run()
