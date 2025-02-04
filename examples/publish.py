import asyncio
import nats

# See https://docs.synternet.com/build/dl-access-points
NATS_URL = "nats://broker-eu-01.synternet.com"
STREAM_SUBJECT = "synternet.example.subject"

async def main():
    nc = await nats.connect(NATS_URL, user_credentials="nats.creds")

    for i in range(1000):
        await nc.publish(STREAM_SUBJECT, (str(i) + "x ").encode('utf-8'))
        await asyncio.sleep(1)

    # Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())
