import grpc
import asyncio
import contextlib
from uno_server import UnoServer
from grpc_health.v1._async import HealthServicer, _health_pb2_grpc
from unoserver import comparer, converter
from v1 import service_pb2_grpc, service_pb2


class GRPCUnoServerServiceServicer(service_pb2_grpc.UnoServerServiceServicer):
    def __init__(
            self,
            uno_interface="127.0.0.1",
            uno_port="2002",
            logger=None,
    ):
        self.uno_interface = uno_interface
        self.uno_port = uno_port
        self.logger = logger

    async def Convert(self, request: service_pb2.ConvertRequest, context):
        conv = converter.UnoConverter(
            interface=self.uno_interface, port=self.uno_port
        )

        # Workaround protobof optionals not working automatically in Python.
        inpath = None
        if request.HasField("inpath"):
            inpath = request.inpath

        indata = None
        if request.HasField("indata"):
            indata = request.indata

        outpath = None
        if request.HasField("outpath"):
            outpath = request.outpath

        filtername = None
        if request.HasField("filtername"):
            filtername = request.filtername

        infiltername = None
        if request.HasField("infiltername"):
            infiltername = request.infiltername

        result = conv.convert(
            inpath,
            indata,
            outpath,
            request.convert_to,
            filtername,
            request.filter_options,
            request.update_index,
            infiltername,
        )

        return service_pb2.ConvertResponse(
            outdata=result
        )

    async def Compare(self, request: service_pb2.CompareRequest, context):
        comp = comparer.UnoComparer(
            interface=self.uno_interface, port=self.uno_port
        )

        # Workaround protobof optionals not working automatically in Python.
        oldpath = None
        if request.HasField("oldpath"):
            oldpath = request.oldpath

        olddata = None
        if request.HasField("olddata"):
            olddata = request.olddata

        newpath = None
        if request.HasField("newpath"):
            newpath = request.newpath

        newdata = None
        if request.HasField("newdata"):
            newdata = request.newdata

        outpath = None
        if request.HasField("outpath"):
            outpath = request.outpath

        filetype = None
        if request.HasField("filetype"):
            filetype = request.filetype

        result = comp.compare(
            oldpath,
            olddata,
            newpath,
            newdata,
            outpath,
            filetype
        )

        return service_pb2.CompareResponse(outdata=result)


class GRPCServer(UnoServer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loop = asyncio.get_event_loop()
        self.grpc_server = grpc.aio.server(
            options=(
                ("grpc.max_send_message_length", 20 * 1024 * 1024),
                ("grpc.max_receive_message_length", 20 * 1024 * 1024),
            )
        )
        self.grpc_server.add_insecure_port(f"{self.interface}:{self.port}")

        _health_pb2_grpc.add_HealthServicer_to_server(HealthServicer(), self.grpc_server)
        service_pb2_grpc.add_UnoServerServiceServicer_to_server(GRPCUnoServerServiceServicer(
            uno_interface=self.uno_interface,
            uno_port=self.uno_port,
            logger=self.logger
        ), self.grpc_server)

        self.cleanup_coroutines = []

    async def run_server(self):
        await self.grpc_server.start()
        self.logger.info("gRPC server started")

        async def server_graceful_shutdown():
            self.logger.info("Starting graceful shutdown...")
            # Shuts down the server with 60 seconds of grace period. During the
            # grace period, the server won't accept new connections and allow
            # existing RPCs to continue within the grace period.
            await self.grpc_server.stop(60)

        self.cleanup_coroutines.append(server_graceful_shutdown())
        await self.grpc_server.wait_for_termination()

    def start(self, **kwargs):
        super().start()
        self.logger.info(f"Starting gRPC server on {self.interface}:{self.port}.")
        with contextlib.suppress(KeyboardInterrupt):
            self.loop.run_until_complete(self.run_server())
        self.loop.run_until_complete(*self.cleanup_coroutines)
        self.loop.close()
