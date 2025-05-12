# AIM
AIM Take Home Assignment

## Table of Contents
1. [Requirements](#requirements)
2. [API Definition](#api-definition)
3. [Tasks](#tasks)
4. [Setup and Running App](#setup-and-running-app)
5. [Deliverables](#deliverables)

## Requirements

This calibration exercise is used to evaluate your skills to work on production code with the team
and therefore is expected to be fully functional, documented, and tested. Aiming for the most
realistic calibration possible, we will evaluate the results as if this was your mini starter project
on day one at AIM. In addition to achieving high-quality results with elegant production code, we
value creative and innovative solutions that generalize well.

Your task is to **create a skeleton of a GRPC service with the proto definition provided below +
simple frontend UI to interact with the service**. While the server needs to implement the GRPC
methods exactly as given, we leave it to you to make design decisions and select the right
framework to enable compatibility with a wide range of platforms and devices. For example, you
can create the backend service in python and the UI as an elegant web app. Or, you can do the
whole thing in javascript, or something else!

**Your system needs to** 
1. Visualize an arbitrary number of robots (each robot is an instance of `Machine` below) on an interactive map in GPS space, for example leveraging Google Maps as
canvas.
2. When left alone, each robot moves in random brownian motion around the map when unpaused, but can be paused via the UI to freeze.
3. It can also be unpaused to resume moving around.

## API Definition
```proto
syntax = "proto3";

message Machine {
  uint32 id = 1;
  GPS location = 2;
  float fuel_level = 3;
  bool is_paused = 4;
}

message GPS {
    double lat = 1;
    double lon = 2;
    float alt = 3;
}

message MachineStreamRequest {}

// gRPC schema definition
service MachineMap {
  rpc Pause(Machine) returns (Machine) {}
  rpc UnPause(Machine) returns (Machine) {}
  rpc MachineStream(MachineStreamRequest) returns (stream Machine) {}
}
```

## Tasks
1. Backend
  - [x] Implement gRPC skeleton service
  - [x] Create brownian motion randomization algorithm
  - [x] Implement `Pause` rpc
  - [x] Implement `UnPause` rpc
  - [x] Implement `MachineStream` rpc
  - [x] Test with gRPC client utility
2. Frontend
  - [x] Implement skeleton UI with canvas
  - [x] Incorporate Maps into canvas
  - [x] Handle onClick for pausing and unpausing robot that is clicked on in canvas
  - [x] Websocket and REST client
3. API
  - [x] Implement websocket server
  - [x] Implement Express server and combine with websocket server
  - [x] Add gRPC client
  - [x] Implement both ws and rest endpoints
5. Environment
  - [x] Configure client Dockerfile for UI image
  - [x] Configure server Dockerfile for gRPC API image
  - [x] Configure api Dockerfile
  - [x] Create Docker compose deployment
6. Testing
  - [x] Test gRPC server with utility
  - [x] Integration testing end-to-end
  - [x] Test on mobile browser
7. Finishing touches
  - [x] Cleanup client with comments
  - [x] Cleanup api with comments
  - [x] Cleanup server with comments
  - [x] Finalize README.md


## Setup and Running App

Running this app only requires Docker on the host and a web browser.

1. Unzip archive of project
2. Enter project root directory in terminal with `cd <./path/to/project>`
3. Deploy app containers with `docker compose up`
4. In web browser visit the IP address of the server host on port 4173 (`localhost:4173` if using browser on same machine)

## Developer Notes

To experiment with the project, before running `docker compose up`, make a `.env` file with the following fields to experiment with:

```sh
NUM_MACHINES=100
CENTER_LAT=39.8283 # determines center of map y in degrees
CENTER_LON=-98.5795 # determines center of map x in degrees
DELTA=0.25 # determines variance in movement along path
NUM_STEPS=100000 # determines path of random walk
MAP_X=5.0 # determines range of movement
MAP_Y=15.0 # determines range of movement
```

Only real flaw with this is that the UI render state is a bit janky and as a result the movement of the robots get delayed. They still move and pause and unpause, but it is delayed before movement starts and it seems to have the updates buffered. That will have to be re explored.

I opted not to use the altitude field because 1, I would need a pre defined 3D mesh of the terrain that the backend has knowledge of, and 2 I couldn't find a maps UI library that makes use of altitude anway.

## Deliverables
Once you have built your solution, please submit an archive containing:
- [x] A working application (we will be trying it out and extensively testing it programmatically) which runs on the most common mobile browsers (Safari, Chrome for Android, etc).
- [x] Your project's source code (stripped of dependencies).
- [x] A readme file which describes how to set-up and run the application (automated
environment setup is a plus).
