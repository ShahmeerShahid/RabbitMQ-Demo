import aio_pika
import asyncio
import json


async def publish_grades(
    tid: int, grades: int, channel
):  # grades is int as placeholder
    grades_json = json.dumps({"tid": tid, "grades": grades})
    await channel.default_exchange.publish(
        aio_pika.Message(grades_json.encode()), routing_key="grades"
    )
