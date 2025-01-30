import os
import asyncio
import tempfile
import nats

from helper import create_app_jwt

ACCESS_TOKEN = "EXAMPLE_ACCESS_TOKEN"

async def main():
    jwt = create_app_jwt(ACCESS_TOKEN)

    # Write the JWT to a temporary file with correct format
    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as temp:
        temp.write(jwt)
        temp_path = temp.name

    nc = await nats.connect("nats://127.0.0.1", user_credentials=temp_path)

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print("Received a message on '{subject}: {data}".format(
            subject=subject, data=data))

    await nc.subscribe("synternet.example.subject", cb=message_handler)

    # run infinitely
    while True:
        await asyncio.sleep(1)

    # Terminate connection to NATS.
    await nc.drain()

    # Delete the temporary file
    os.unlink(temp_path)

if __name__ == '__main__':
    asyncio.run(main())
