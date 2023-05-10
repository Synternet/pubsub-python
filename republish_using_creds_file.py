import asyncio
import nats


async def main():
    nc = await nats.connect("nats://127.0.0.1", user_credentials="nats.creds")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print("Received a message on '{subject}: {data}".format(
            subject=subject, data=data))
        await nc.publish("syntropy.test.subject", msg.data)

    await nc.subscribe("syntropy.bitcoin.tx", cb=message_handler)

    # run infinitely
    while True:
        await asyncio.sleep(1)

    # Remove interest in subscription.
    await sub.unsubscribe()

    # Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())
