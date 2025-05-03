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
  - [ ] Implement gRPC skeleton service
  - [ ] Create brownian motion randomization algorithm
  - [ ] Implement `Pause` rpc
  - [ ] Implement `UnPause` rpc
  - [ ] Implement `MachineStream` rpc
  - [ ] Test with gRPC client utility
2. Frontend
  - [ ] Implement skeleton UI with canvas
  - [ ] Incorporate Google Maps into canvas
  - [ ] Handle onClick for pausing and unpausing robot that is clicked on in canvas
  - [ ] Incorporate gRPC client
  - [ ] Use NGINX to host UI and proxy requests
3. gRPC Envoy Proxy
  - [ ] Configure Envoy proxy
  - [ ] Integrate with UI
  - [ ] End to end test UI talking to backend through proxy
5. Environment
  - [ ] Configure client Dockerfile for UI image
  - [ ] Configure server Dockerfile for gRPC API image
  - [ ] Configure gRPC proxy Dockerfile
  - [ ] Create Docker compose deployment


## Setup and Running App

Running this app only requires Docker and a web browser.

1. Unzip archive of project
2. Enter project root directory in terminal with `cd <./path/to/project>`
3. Deploy app containers with `docker compose up`
4. In web browser visit the IP address of the server host on port 8000 (`localhost:8000` if using browser on same machine)

## Deliverables
Once you have built your solution, please submit an archive containing:
- [ ] A working application (we will be trying it out and extensively testing it programmatically) which runs on the most common mobile browsers (Safari, Chrome for Android, etc).
- [x] Your project's source code (stripped of dependencies).
- [x] A readme file which describes how to set-up and run the application (automated
environment setup is a plus).

...
