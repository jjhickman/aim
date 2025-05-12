import { LatLngTuple, Icon } from "leaflet";
import { MapContainer, Marker, TileLayer, useMap, Popup } from "react-leaflet";
import React from "react";
import { Machine } from "./machine";
import "leaflet/dist/leaflet.css";

const CENTER_COORDS: LatLngTuple = [39.8283, -98.5795];
const ROBOT_ICON = new Icon({
  iconUrl: "robot.svg",
  iconSize: [35, 35], // size of the icon
  iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
  popupAnchor: [-3, -76], // point from which the popup should open relative to the iconAnchor
});

function ResizeMap() {
  const map = useMap();
  map.invalidateSize();
  return null;
}

type CustomMachineMap = {
  [key: number]: Machine;
}


export default function CanvasMap() {
  const [machines, setMachines] = React.useState<CustomMachineMap>({});

  const pause = React.useCallback(async (machine: Machine) => {
    console.log("PAUSING");
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(machine),
    };
    const response = await fetch(
      `http://${window.location.hostname}:8000/api/pause`,
      options
    );
    console.log(response);
  }, []);

  const handleClick = React.useCallback((machine: Machine) =>
    machine.isPaused ? unPause(machine) : pause(machine), []);

  const unPause = React.useCallback(async (machine: Machine) => {
    console.log("MOVING");
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(machine),
    };
    const response = await fetch(
      `http://${window.location.hostname}:8000/api/unpause`,
      options
    );
    console.log(response);
  }, []);

  React.useEffect(() => {
    const stream = new WebSocket(`ws://${window.location.hostname}:8000`);
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
      const machine: Machine = JSON.parse(message.data);
     setMachines(
        (prevState) => {
          return {...prevState, [machine.id]: machine}
        })
      /*setMachines(
        (prevState) => new Map([...prevState.entries(), [machine.id, machine]])
      );
      */
    };
    return () => stream.close();
  }, []);

  return (
    <div style={{ width: "100%", height: "50vh" }}>
      <MapContainer
        center={CENTER_COORDS}
        zoom={7}
        scrollWheelZoom={false}
        placeholder={<img src="placeholder.jpg" alt="placeholder" />}
        style={{ width: "100%", height: "100%" }}
      >
        <ResizeMap />
        <TileLayer
          id="tile"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {Object.values(machines).map((machine: Machine) => {
          return (
            <Marker
              eventHandlers={{
                click: () => handleClick(machine),
              }}
              position={[
                machine.location?.lat ?? CENTER_COORDS[0],
                machine.location?.lon ?? CENTER_COORDS[1],
              ]}
              key={machine.id.toString()}
              icon={ROBOT_ICON}
            >
              {machine.fuelLevel <= 0 && (
                <Popup>{`Machine ${machine.id} is out of fuel`}</Popup>
              )}
              {machine.isPaused && (
                <Popup>{`Machine ${machine.id} is paused`}</Popup>
              )}
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}
