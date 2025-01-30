import asyncio
import nats

async def main():
    nc = await nats.connect("nats://127.0.0.1", user_credentials="nats.creds")

    for i in range(1000):
        await nc.publish("my_publisher.example.subject", (str(i) + "x ").encode('utf-8'))
        await asyncio.sleep(1)

    # Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())
