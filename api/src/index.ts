import { ChannelCredentials } from '@grpc/grpc-js'
import { GrpcTransport } from '@protobuf-ts/grpc-transport';
import { WebSocketServer } from 'ws';
import { Machine, MachineStreamRequest } from "./machine";
import { MachineMapClient } from "./machine.client";
import app from './app';

const gRPCtransport = new GrpcTransport({
    host: "server:50051",
    channelCredentials: ChannelCredentials.createInsecure(),
});
const client = new MachineMapClient(gRPCtransport);
const server = app.listen(8000, () => { console.log('Server listening on port 8000'); });
const wss = new WebSocketServer({ server });

wss.on('connection', async (ws) => {
    const request: MachineStreamRequest = {};
    let stream = client.machineStream(request);
    ws.on('error', console.error);
    ws.on('message', (data) => {
        console.log(`New websocket message ${data}`);
    });
    for await (let machine of stream.responses) {
        ws.send(JSON.stringify(machine));
    }
});

