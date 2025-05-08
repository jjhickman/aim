import { LatLngTuple } from "leaflet";
import { MapContainer, Marker, TileLayer } from "react-leaflet";
import { MachineMapClient, Machine, MachineStreamRequest } from "./machine";
import React from "react";

const CENTER_COORDS: LatLngTuple = [
  Number(process.env.CENTER_LAT ?? "71.0565"),
  Number(process.env.CENTER_LON ?? "42.3555")
];

const ENVOY_URL = process.env.ENVOY_URL ?? "127.0.0.1:8000"
const machineClient = new MachineMapClient(ENVOY_URL)

export default function CanvasMap() {
  const [ machines, setMachines ] = React.useState<Machine[]>([]);
  const [ numMachines, setNumMachines ] = React.useState<number>(0);

  const pause = React.useCallback(async (machine: Machine) => {
    const request = new Machine(machine);
    const response = await machineClient.Pause(request, {});
    console.log(response);
  }, []);

  const unPause = React.useCallback(async (machine: Machine) => {
    if (machine.fuel_level === 0) {
      console.log(`Cannot move machine ${machine.id} - out of gas`)
    }
    const request = new Machine(machine);
    const response = await machineClient.UnPause(request, {});
    console.log(response);
  }, []);

  const streamMachines = React.useCallback(() => {
    const request = new MachineStreamRequest();
    const stream = machineClient.MachineStream(request, {});
    stream.on('data', (response: Machine) => {
      console.log(response);
      if (numMachines > response.id) {
        setMachines( prevState => [
          ...prevState.slice(0, response.id),
          {
              ...prevState[response.id],
              ...response,
          } as Machine,
          ...prevState.slice(response.id + 1)
      ]);
      } else if (numMachines === response.id) {
        setMachines(prevState => [...prevState, response])
      }
    });
    stream.on('end', () => {
      // stream end signal
      stream.cancel();
    });
  }, [numMachines]);

  React.useEffect(() => {
    setNumMachines(machines.length);
  }, [machines]);

  React.useEffect(() => {
    streamMachines();
  }, [streamMachines]);

  return (
    <MapContainer center={CENTER_COORDS} zoom={13} scrollWheelZoom={false}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {machines.length > 0 && machines.map((machine, index) => {
        return (<div onClick={machine.is_paused ? () => unPause(machine) : () => pause(machine)}>
          <Marker position={[machine.location.lat, machine.location.lon]} key={index.toString()}/>
        </div>);
      })}
    </MapContainer>
  );
}