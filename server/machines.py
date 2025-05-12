import numpy as np
import random
import machine_pb2
import os
import logging
import brownian
class Machines:
    # Class variable
    num_machines = 0
    machines = []
    machines_paths = []
    map_x = 10
    map_y = 10
    center_lon = 0
    center_lat = 0
    delta = 0.01
    num_steps = 5000
    mileage = 0.0

    def __init__(self, num_machines, center_lon, center_lat, delta, num_steps):
        self.machines = []
        self.machines_paths = []
        self.num_machines = num_machines
        self.center_lon = center_lon
        self.center_lat = center_lat
        self.delta = delta
        self.num_steps = num_steps
        self.mileage = 100.0/num_machines
        map_x_str = os.environ.get("MAP_X")
        map_y_str = os.environ.get("MAP_Y")
        if map_x_str is None or not map_x_str.isnumeric():
            self.map_x = 5.0
        else:
            self.map_x = float(map_x_str)
        if map_y_str is None or not map_y_str.isnumeric():
            self.map_y = 15.0
        else:
            self.map_y = float(map_y_str)
        self.generate_machines()

    def generate_machines(self):
        """Initialized list of machines, with id serving as index"""
        logging.info(f"Generating {self.num_machines} machines")
        for index in range(self.num_machines):
            lat = self.center_lat + random.uniform(-(self.map_x / 2), self.map_x / 2)
            lon = self.center_lon + random.uniform(-(self.map_y / 2), self.map_y / 2)
            gps = machine_pb2.GPS(alt=0, lat=lat, lon=lon)
            new_machine = machine_pb2.Machine(id=index, location=gps, fuel_level = 100.0, is_paused=False)
            self.machines.append(new_machine)

            path = np.empty((2,self.num_steps+1))
            path[0, 0] = lat
            path[1, 0] = lon
            brownian.brownian(path[:,0], self.num_steps, self.mileage, self.delta, out=path[:,1:])
            self.machines_paths.append(path)

    def unpause_machine(self, id):
        if id >= len(self.machines):
            logging.error(f"Machine with id {id} exceeds range")
            return self.machines[-1]
        elif self.machines[id].fuel_level <= 0:
            logging.error(f"Machine {id} is out of fuel")
            return self.machines[id]
        updated_machine = machine_pb2.Machine(id=id, location=self.machines[id].location, fuel_level = self.machines[id].fuel_level, is_paused=False)
        return self.machines[id]

    def pause_machine(self, id):
        if id >= len(self.machines):
            logging.info(f"Machine with id {id} exceeds range")
            return self.machines[-1]
        elif self.machines[id].is_paused:
            logging.info(f"Machine {id} is already paused, toggling")
            updated_machine = machine_pb2.Machine(id=id, location=self.machines[id].location, fuel_level = self.machines[id].fuel_level, is_paused=False)
        else:
            updated_machine = machine_pb2.Machine(id=id, location=self.machines[id].location, fuel_level = self.machines[id].fuel_level, is_paused=True)
        self.machines[id] = updated_machine
        return self.machines[id]

    def get_machine(self, id):
        if id >= len(self.machines):
            logging.error(f"Machine with id {id} exceeds range")
            return self.machines[-1]
        return self.machines[id]

    def update_locations(self):
        for id in range(len(self.machines)):
            if self.machines[id].is_paused:
                logging.info(f"Machine {id} is paused")
                continue
            elif self.machines[id].fuel_level > 0 and len(self.machines_paths[id]) == 2:
                    path = self.machines_paths[id]
                    lat = path[0,0]
                    lon = path[1,0]
                    gps = machine_pb2.GPS(alt=0, lat=lat, lon=lon)
                    updated_machine = machine_pb2.Machine(id=id, location=gps, fuel_level = self.machines[id].fuel_level - self.mileage, is_paused=False)
                    self.machines[id] = updated_machine
                    self.machines_paths[id] = np.delete(self.machines_paths[id], 0)