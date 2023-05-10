import asyncio
import nats
import tempfile
import os

from helper import create_app_jwt

dapp_access_token = "SAAGNJOZTRPYYXG2NJX3ZNGXYUSDYX2BWO447W3SHG6XQ7U66RWHQ3JUXM"

async def main():
    jwt = create_app_jwt(dapp_access_token)

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
        # await nc.publish("syntropy.test.subject", msg.data)

    await nc.subscribe("syntropy.bitcoin.tx", cb=message_handler)

    # run infinitely
    while True:
        await asyncio.sleep(1)

    # Terminate connection to NATS.
    await nc.drain()

    # Delete the temporary file
    os.unlink(temp_path)

if __name__ == '__main__':
    asyncio.run(main())