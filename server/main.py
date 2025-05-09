from grpc import aio
import nest_asyncio
import asyncio
import logging
import sys
import os

sys.path.append(".")
import machine_pb2_grpc
import machines

nest_asyncio.apply()
class MachineService(machine_pb2_grpc.MachineMapServicer):
    
    m = None
    mutex = asyncio.Lock()
    def __init__(self):
        self.create()

    def create(self):
        num_machines_str = os.environ.get("NUM_MACHINES")
        center_lon_str = os.environ.get("CENTER_LON")
        center_lat_str = os.environ.get("CENTER_LAT")
        delta_str = os.environ.get("DELTA")
        max_alt_str = os.environ.get("MAX_ALT")
        num_machines = 0
        center_lon = 0
        center_lat = 0
        delta = 0.0
        max_alt = 0
        if num_machines_str is None or not num_machines_str.isnumeric():
            num_machines = 100
        else:
            num_machines = int(num_machines_str)

        if center_lon_str is None or not center_lon_str.isnumeric():
            center_lon = -50
        else:
            center_lon = float(center_lon_str)

        if center_lat_str is None or not center_lat_str.isnumeric():
            center_lat = 50
        else:
            center_lon = float(center_lat_str)

        if delta_str is None or not delta_str.isnumeric():
            delta = 0.0001
        else:
            delta = float(delta_str)

        if max_alt_str is None or not max_alt_str.isnumeric():
            max_alt = 1000
        else:
            max_alt = float(max_alt_str)
        self.m = machines.Machines(num_machines=num_machines, center_lon=center_lon, center_lat=center_lat, delta=delta, max_alt=max_alt)
        asyncio.create_task(self.move_machines())
            
    async def move_machines(self):
        logging.info("Starting async movement update loop")
        while True:
            await asyncio.sleep(0.5)
            await self.mutex.acquire()
            try:
                self.m.update_locations()
            finally:
                self.mutex.release()

    async def Pause(self, request, context):
        """Pause machine by specified id in the request if it is moving"""
        await self.mutex.acquire()
        try:
            logging.info(f"Pausing machine {request.id}")
            updated_machine = self.m.pause_machine(request.id)
            return updated_machine
        finally:
            self.mutex.release()

    async def UnPause(self, request, context):
        """UnPause machine by specified id in the request if it is stationary"""
        await self.mutex.acquire()
        try:
            logging.info(f"Moving machine {request.id}")
            updated_machine = self.m.unpause_machine(request.id)
            return updated_machine
        finally:
            self.mutex.release()

    async def MachineStream(
        self,
        request_iterator,
        context,
    ):
        """Stream machines one at a time with updated locations per request iterable"""
        logging.info("Starting machine stream")
        index = 0
        while True:
            await asyncio.sleep(0.5)
            logging.debug(f"Streaming machine {index}")
            await self.mutex.acquire()
            try:
                yield self.m.get_machine(index)
            finally:
                self.mutex.release()
                index = index + 1 % self.m.num_machines

async def serve():                                                      
    server = aio.server() 
    machine_pb2_grpc.add_MachineMapServicer_to_server(MachineService(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("Server started. Awaiting jobs...")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)                                     
    asyncio.run(serve())