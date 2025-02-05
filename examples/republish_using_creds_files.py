import asyncio
import nats

# See https://docs.synternet.com/build/dl-access-points
NATS_URL = "nats://broker-eu-01.synternet.com"
SUB_SUBJECT = "synternet.example.subject"
PUB_SUBJECT = "republisher.example.subject"

async def main():
    sub_nc = await nats.connect(NATS_URL, user_credentials="subscriber_nats.creds")
    pub_nc = await nats.connect(NATS_URL, user_credentials="publisher_nats.creds")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print("Received a message on '{subject}: {data}".format(
            subject=subject, data=data))
        await pub_nc.publish(PUB_SUBJECT, msg.data)

    await sub_nc.subscribe(SUB_SUBJECT, cb=message_handler)

    # run infinitely
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
