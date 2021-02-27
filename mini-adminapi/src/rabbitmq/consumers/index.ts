import { Channel } from "amqplib";

export async function setupRabbitMQConsumers(channelPromise: Promise<Channel>) {
	const channel = await channelPromise;

	channel.assertQueue("logs");
	channel.consume("logs", (message) => {
		if (message == null) throw Error("Null message received in log queue");
        console.log({logMessage: JSON.parse(message.content.toString())})
        channel.ack(message)
	});

    channel.assertQueue("grades");
    channel.consume("grades", (message) => {
        if (message == null) throw Error("Null message received in grades queue")
        console.log({gradesMessage: JSON.parse(message.content.toString())})
        channel.ack(message)
    })
}
