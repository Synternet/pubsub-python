import asyncio
import nats

NATS_URL = "nats://127.0.0.1"

async def main():
    sub_nc = await nats.connect(NATS_URL, user_credentials="subscriber_nats.creds")
    pub_nc = await nats.connect(NATS_URL, user_credentials="publisher_nats.creds")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print("Received a message on '{subject}: {data}".format(
            subject=subject, data=data))
        await pub_nc.publish("republisher.example.subject", msg.data)

    await sub_nc.subscribe("synternet.example.subject", cb=message_handler)

    # run infinitely
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
