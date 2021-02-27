import asyncio
import aio_pika
import time
import random
import os
import logger
import grades


def create_process_task_fn(channel: aio_pika.RobustChannel):

    # Return a function that takes in a message with channel curried into it
    async def process_task(message: aio_pika.IncomingMessage):
        async with message.process():
            await logger.log_message(f"Received task: {message.body}", channel)
            await grade_task(channel)

    return process_task


async def grade_task(channel: aio_pika.RobustChannel):
    tid = random.randint(0, 10)
    await logger.log_message(f"Initiating grading for task {tid}", channel)
    time.sleep(5)  # this represents the automarker running
    await logger.log_message(f"Grading complete for task {tid}", channel)

    await grades.publish_grades(tid, random.randint(0, 100), channel)


async def main(loop, username="guest", password="guest", host="rabbitmq"):
    connection = await aio_pika.connect_robust(
        host=host, login=username, password=password, loop=loop
    )

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be
    # processing at the same time.
    await channel.set_qos(prefetch_count=5)

    # Declaring queues
    tasks_queue = await channel.declare_queue("tasks", durable=True)

    await tasks_queue.consume(create_process_task_fn(channel))

    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    rabbitmq_host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    rabbitmq_username = os.environ.get("RABBITMQ_USERNAME", "guest")
    rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD", "guest")

    connected = False
    while not connected:
        print("Attempting to connect to rabbitmq instance")
        try:
            connection = loop.run_until_complete(
                main(
                    loop,
                    host=rabbitmq_host,
                    username=rabbitmq_username,
                    password=rabbitmq_password,
                )
            )
        except ConnectionError:
            print("Connection failed, retrying in 5 seconds")
            time.sleep(5)
            continue

        print("Successfully connected to rabbitmq instance 🐇")
        connected = True

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
