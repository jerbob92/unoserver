class UnoServer:
    def __init__(
            self,
            interface="127.0.0.1",
            port="2003",
            uno_interface="127.0.0.1",
            uno_port="2002",
            version=None,
            logger=None,
    ):
        self.interface = interface
        self.port = port
        self.uno_interface = uno_interface
        self.uno_port = uno_port
        self.version = version
        self.logger = logger

    def start(self):
        self.logger.info(f"Starting unoserver {self.version}.")

