import aio_pika
import asyncio
import json


async def log_message(message, channel):
    print(message)
    log_json = json.dumps({"source": "automarker", "message": message})
    await channel.default_exchange.publish(
        aio_pika.Message(log_json.encode()), routing_key="logs"
    )
