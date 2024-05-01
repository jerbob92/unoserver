import argparse
import logging
import subprocess
import sys
import tempfile
from importlib import metadata
from pathlib import Path
from libreoffice import LibreOfficeServer
from xmlrpc_server import XMLRPCServer
from grpc_server import GRPCServer

__version__ = metadata.version("unoserver")

logger = logging.getLogger("unoserver")


def main():
    logging.basicConfig()
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser("unoserver")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Display version and exit.",
        version=f"{parser.prog} {__version__}",
    )
    parser.add_argument(
        "--interface",
        default="127.0.0.1",
        help="The interface used by the XMLRPC server",
    )
    parser.add_argument(
        "--uno-interface",
        default="127.0.0.1",
        help="The interface used by the Libreoffice UNO server",
    )
    parser.add_argument(
        "--port", default="2003", help="The port used by the XMLRPC or gRPC server"
    )
    parser.add_argument(
        "--uno-port", default="2002", help="The port used by the Libreoffice UNO server"
    )
    parser.add_argument("--daemon", action="store_true", help="Deamonize the server")
    parser.add_argument(
        "--executable",
        default="libreoffice",
        help="The path to the LibreOffice executable",
    )
    parser.add_argument(
        "--user-installation",
        default=None,
        help="The path to the LibreOffice user profile",
    )
    parser.add_argument(
        "--libreoffice-pid-file",
        "-p",
        default=None,
        help="If set, unoserver will write the Libreoffice PID to this file. If started "
        "in daemon mode, the file will not be deleted when unoserver exits.",
    )
    parser.add_argument(
        "--protocol",
        default="xmlrpc",
        choices=["xmlrpc", "grpc"],
        help="The protocol to use",
    )
    args = parser.parse_args()

    if args.daemon:
        cmd = sys.argv
        cmd.remove("--daemon")
        proc = subprocess.Popen(cmd)
        return proc.pid

    with tempfile.TemporaryDirectory() as tmpuserdir:
        user_installation = Path(tmpuserdir).as_uri()

        if args.user_installation is not None:
            user_installation = Path(args.user_installation).as_uri()

        if args.uno_port == args.port:
            raise RuntimeError("--port and --uno-port must be different")

        libre_office_server = LibreOfficeServer(
            user_installation=user_installation,
            uno_port=args.uno_port,
            uno_interface=args.uno_interface,
            executable=args.executable,
            version=__version__,
            logger=logger
        )
        libre_office_server.start()

        if args.protocol == "xmlrpc":
            server = XMLRPCServer(
                interface=args.interface,
                port=args.port,
                uno_port=args.uno_port,
                uno_interface=args.uno_interface,
                version=__version__,
                logger=logger
            )
        elif args.protocol == "grpc":
            server = GRPCServer(
                interface=args.interface,
                port=args.port,
                uno_port=args.uno_port,
                uno_interface=args.uno_interface,
                version=__version__,
                logger=logger
            )
        else:
            raise RuntimeError("unknown protocol")

        # This will block until shutdown.
        server.start()
        libre_office_server.shutdown()
        logger.info("Server has shutdown")

if __name__ == "__main__":
    main()
