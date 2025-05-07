import numpy as np
import random
import machine_pb2
import os

class Machines:
    # Class variable
    num_machines = 0
    machines = []
    map_x = 10
    map_y = 10
    max_alt = 0
    center_lon = 0
    center_lat = 0
    delta = 0.001

    def __init__(self, num_machines, center_lon, center_lat, delta, max_alt):
        self.machines = []
        self.num_machines = num_machines
        self.center_lon = center_lon
        self.center_lat = center_lat
        self.delta = delta
        self.max_alt = max_alt
        map_x_str = os.environ("MAP_X", "20.0")
        map_y_str = os.environ("MAP_Y", "20.0")
        if not map_x_str.isnumeric():
            self.map_x = 20.0
        else:
            self.map_x = float(map_x_str)
        if not map_y_str.isnumeric():
            self.map_y = 20.0
        else:
            self.map_y = float(map_y_str)
        self.generate_machines()

    def generate_machines(self):
        print(f"Generating {self.num_machines} machines")
        for index in range(self.num_machines):
            lat = self.center_lat + random.uniform(-(self.map_x / 2), self.map_x / 2)
            lon = self.center_lon + random.uniform(-(self.map_y / 2), self.map_y / 2)
            alt = random.uniform(0, self.max_alt)
            gps = machine_pb2.GPS(alt=alt, lat=lat, lon=lon)
            new_machine = machine_pb2.Machine(id=index, location=gps, fuel_level = 100.0, is_paused=False)
            self.machines.append(new_machine)

    def unpause_machine(self, id):
        if id >= len(self.machines):
            print(f"Machine with id {id} exceeds range")
            return machine_pb2.Machine()
        elif not self.machines[id].is_paused:
            print(f"Machine {id} is already in motion")
        elif self.machines[id].fuel_level <= 0:
            print(f"Machine {id} is out of fuel")
        else:
            self.machines[id].is_paused = False
        return self.machines[id]

    def pause_machine(self, id):
        if id >= len(self.machines):
            print(f"Machine with id {id} exceeds range")
            return machine_pb2.Machine()
        elif self.machines[id].is_paused:
            print(f"Machine {id} is already paused")
        self.machines[id].is_paused = True
        return self.machines[id]

    def random_movement(self, machine):
        p1 = np.array([machine.location.lat, machine.location.lon, machine.location.lat])

        lat = machine.location.lat + random.uniform(-self.delta, self.delta)
        lon = machine.location.lon + random.uniform(-self.delta, self.delta)
        alt = machine.location.alt + random.uniform(-self.delta, self.delta)

        if lat > self.center_lat + self.map_x / 2:
            lat = self.center_lat + self.map_x / 2
        elif lat < self.center_lat - self.map_x / 2:
            lat = self.center_lat - self.map_x / 2

        if lon < self.center_lon - self.map_y / 2:
            lon = self.center_lon + self.map_y / 2
        elif lon < self.center_lon - self.map_y / 2:
            lon = self.center_lat - self.map_y / 2

        if alt < 0:
            alt = 0
        elif alt > self.max_alt:
            alt = self.max_alt
        p2 = np.array([lat, lon, alt])
        squared_dist = np.sum((p1-p2)**2, axis=0)
        dist = np.sqrt(squared_dist) / 1000

        gps = machine_pb2.GPS(alt=alt, lat=lat, lon=lon)
        self.machines[machine.id].location.CopyFrom(gps)
        self.machines[machine.id].fuel_level -= dist
        if self.machines[machine.id].fuel_level <= 0:
            self.machines[machine.id].fuel_level = 0
            self.machines[machine.id].is_paused = True

        return self.machines[machine.id]

    def update_location(self, id):
        if id >= len(self.machines):
            print(f"Machine with id {id} exceeds range")
            return None
        elif self.machines[id].is_paused:
            print(f"Machine {id} is paused")
            return None
        return self.random_movement(self.machines[id])