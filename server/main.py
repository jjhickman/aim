from concurrent import futures
import grpc
import time
import sys
import os

sys.path.append(".")
import machine_pb2_grpc
import machines

class MachineService(machine_pb2_grpc.MachineMapServicer):
    
    m = None
    def __init__(self):
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

    def Pause(self, request, context):
        """Pause machine by specified id in the request if it is moving"""
        print(f"Pausing machine {request.id}")
        updated_machine = self.m.pause_machine(request.id)
        self.m.update_locations() # for simplicity, only update locations per request
        return updated_machine

    def UnPause(self, request, context):
        """UnPause machine by specified id in the request if it is stationary"""
        print(f"Moving machine {request.id}")
        self.m.update_locations() # for simplicity, only update locations per request
        updated_machine = self.m.unpause_machine(request.id)
        return updated_machine

    def MachineStream(
        self,
        request_iterator,
        context: grpc.ServicerContext,
    ):
        """Stream machines one at a time with updated locations per request iterable"""
        print("Starting machine stream")
        index = 0
        while context.is_active():
            time.sleep(0.1)
            print(f"Streaming machine {index}")
            yield self.m.get_machine(index)
            self.m.update_locations() # for simplicity, only update locations per request
            index = index + 1 % self.m.num_machines

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    machine_pb2_grpc.add_MachineMapServicer_to_server(MachineService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Awaiting jobs...")
    try:
        while True: # since server.start() will not block, a sleep-loop is added to keep alive
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()