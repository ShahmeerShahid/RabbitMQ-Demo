import express from "express";
import cors from "cors";
import morgan from "morgan";
import { Channel } from "amqplib";
import { createClient } from "./rabbitmq/init";
import taskRouter from "./routes/tasks.router"

const app = express();
app.use(cors());
app.use(morgan("common"));
app.use(express.json());

const rabbitmq_host = process.env.RABBITMQ_HOST || "rabbitmq";
const rabbitmq_username = process.env.RABBITMQ_USERNAME || "guest";
const rabbitmq_password123 = process.env.RABBITMQ_PASSWORD || "guest";

const rabbitmqChannelPromise = createClient(
	rabbitmq_host,
	rabbitmq_username,
	rabbitmq_password123
);

// Don't need to do this if not using typescript
declare global {
	namespace Express {
		interface Request {
			rabbitmqChannelPromise: Promise<Channel>;
		}
	}
}

// Add rabbitmqClient to request object for use in middleware
app.use((req, res, next) => {
	req.rabbitmqChannelPromise = rabbitmqChannelPromise;
	next();
});

import {setupRabbitMQConsumers} from "./rabbitmq/consumers/index"
setupRabbitMQConsumers(rabbitmqChannelPromise)

app.get("/", async (req, res) => {
	res.json({ message: "Hello, world!" });
});

app.use("/api/tasks", taskRouter)

const port = process.env.PORT || 8080
app.listen(port, function () {
	console.log(`Server is running on port: ${port}`);
});
