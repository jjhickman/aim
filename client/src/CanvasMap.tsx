import { LatLngTuple } from "leaflet";
import { MapContainer, Marker, TileLayer } from "react-leaflet";
import React from "react";
import { WebSocket } from "ws";
import { Machine } from "./machine";

const CENTER_COORDS: LatLngTuple = [
  Number(process.env.CENTER_LAT ?? "71.0565"),
  Number(process.env.CENTER_LON ?? "42.3555"),
];

export default function CanvasMap() {
  const [machines, setMachines] = React.useState<Machine[]>([]);
  const numMachines = React.useRef<number>(0);

  const pause = React.useCallback(async (machine: Machine) => {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(machine)
    };
    const response = await fetch('http://api:8000/pause', options);
    console.log(response);
  }, []);

  const unPause = React.useCallback(async (machine: Machine) => {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(machine)
    };
    const response = await fetch('http://api:8000/unpause', options);
    console.log(response);
  }, []);

  React.useEffect(() => {    
    const stream = new WebSocket('ws://api:8000');
    stream.onopen = () => {
      console.log(`Websocket stream open`);
    };
    stream.onclose = () => {
      console.log("Connection closed");
    };
    stream.onerror = () => {
      stream.close();
    };
    stream.onmessage = (message) => {
      console.log(message);
      const machine: Machine = JSON.parse(JSON.stringify(message));
      if (numMachines.current > machine.id) {
        setMachines((prevState) => [
          ...prevState.slice(0, machine.id),
          {
            ...prevState[machine.id],
            ...machine,
          } as Machine,
          ...prevState.slice(machine.id + 1),
        ]);
      } else if (numMachines.current === machine.id) {
        setMachines((prevState) => [...prevState, machine]);
        numMachines.current += 1;
      }
    };
    return () => stream.close();
  }, []);

  return (
    <MapContainer center={CENTER_COORDS} zoom={13} scrollWheelZoom={false}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {machines.length > 0 &&
        machines.map((machine, index) => {
          return (
            <div
              onClick={
                machine.isPaused ? () => unPause(machine) : () => pause(machine)
              }
            >
              <Marker
                position={[
                  machine.location?.lat ?? CENTER_COORDS[0],
                  machine.location?.lon ?? CENTER_COORDS[1],
                ]}
                key={index.toString()}
              />
            </div>
          );
        })}
    </MapContainer>
  );
}
