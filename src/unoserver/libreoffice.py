import os
import subprocess


class LibreOfficeServer:
    def __init__(
            self,
            uno_interface="127.0.0.1",
            uno_port="2002",
            user_installation=None,
            version=None,
            logger=None,
            executable="libreoffice",
            libreoffice_pid_file=None,
    ):
        self.user_installation = user_installation
        self.uno_interface = uno_interface
        self.uno_port = uno_port
        self.version = version
        self.logger = logger
        self.executable=executable
        self.libreoffice_process = None
        self.libreoffice_pid_file = libreoffice_pid_file

    def start(self):
        self.logger.info(f"Starting LibreOffice")

        connection = (
                "socket,host=%s,port=%s,tcpNoDelay=1;urp;StarOffice.ComponentContext"
                % (self.uno_interface, self.uno_port)
        )

        # I think only --headless and --norestore are needed for
        # command line usage, but let's add everything to be safe.
        cmd = [
            self.executable,
            "--headless",
            "--invisible",
            "--nocrashreport",
            "--nodefault",
            "--nologo",
            "--nofirststartwizard",
            "--norestore",
            f"-env:UserInstallation={self.user_installation}",
            f"--accept={connection}",
        ]

        self.logger.info("LibreOffice Command: " + " ".join(cmd))
        self.libreoffice_process = subprocess.Popen(cmd)

        pid = self.libreoffice_process.pid
        self.logger.info(f"LibreOffice PID: {pid}")

        if self.libreoffice_pid_file:
            with open(self.libreoffice_pid_file, "wt") as upf:
                upf.write(f"{pid}")

        return

    def shutdown(self):
        pid = self.libreoffice_process.pid

        if self.libreoffice_pid_file:
            # Remove the PID file
            os.unlink(self.libreoffice_pid_file)

        try:
            # Make sure it's really dead
            os.kill(pid, 0)
            # It was killed
            return 0
        except OSError as e:
            if e.errno == 3:
                # All good, it was already dead.
                return 0
            raise
