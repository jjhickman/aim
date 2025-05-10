import { ChannelCredentials } from '@grpc/grpc-js'
import { GrpcTransport} from '@protobuf-ts/grpc-transport';
import express, { NextFunction, Request, Response } from "express";
import cors from "cors";
import helmet from "helmet";
import loggerExpress from "logger";
import { MachineMapClient } from "./machine.client";

const logger = loggerExpress.createLogger();
const app = express();

const gRPCtransport = new GrpcTransport({
    host: "server:50051",
    channelCredentials: ChannelCredentials.createInsecure(),
});
const client = new MachineMapClient(gRPCtransport);

// Security headers
app.use(helmet());

// CORS configuration
app.use(
    cors({
        origin: "http://client:4173",
        methods: ["GET", "POST"],
    }),
);

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// API Routes
app.post('/api/pause', async (req: Request, res: Response) => {
    const pausedMachine = client.pause(req);
    res.status(200).json(pausedMachine);
});

// API Routes
app.post('/api/unpause', async (req: Request, res: Response) => {
    const unPausedMachine = client.unPause(req);
    res.status(200).json(unPausedMachine);
});

// 404
// Routes
app.get("/", (req, res) => {
    res.send("Secure Express Server");
});

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    logger.error(err.stack);
    res.status(500).json({ error: "Internal Server Error" });
});

export default app;