import xmlrpc.server
from uno_server import UnoServer
from unoserver import converter, comparer
import contextlib


class XMLRPCServer(UnoServer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.xmlrcp_server = None

    def start(self, **kwargs):
        super().start()
        self.logger.info(f"Starting XMLRPC server on {self.interface}:{self.port}.")
        with xmlrpc.server.SimpleXMLRPCServer(
                (self.interface, int(self.port)), allow_none=True
        ) as server:
            self.xmlrcp_server = server

            server.register_introspection_functions()

            @server.register_function
            def convert(
                    inpath=None,
                    indata=None,
                    outpath=None,
                    convert_to=None,
                    filtername=None,
                    filter_options=[],
                    update_index=True,
                    infiltername=None,
            ):
                if indata is not None:
                    indata = indata.data
                conv = converter.UnoConverter(
                    interface=self.uno_interface, port=self.uno_port
                )
                result = conv.convert(
                    inpath,
                    indata,
                    outpath,
                    convert_to,
                    filtername,
                    filter_options,
                    update_index,
                    infiltername,
                )
                return result

            @server.register_function
            def compare(
                    oldpath=None,
                    olddata=None,
                    newpath=None,
                    newdata=None,
                    outpath=None,
                    filetype=None,
            ):
                if olddata is not None:
                    olddata = olddata.data
                if newdata is not None:
                    newdata = newdata.data
                comp = comparer.UnoComparer(
                    interface=self.uno_interface, port=self.uno_port
                )
                result = comp.compare(
                    oldpath, olddata, newpath, newdata, outpath, filetype
                )
                return result

            with contextlib.suppress(KeyboardInterrupt):
                server.serve_forever()

            self.logger.info("Starting shutdown...")

            server.shutdown()


