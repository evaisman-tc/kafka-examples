#! /usr/local/bin/python3

# Produce test messages to a topic

import time
import argparse

from kafka import KafkaProducer


def parse():
    """Parse command line"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--brokers', default='kafka:9092', help='Kafka bootstrap brokers')
    parser.add_argument('-t', '--topic', default='test-topic', help='Name of topic to produce to')
    parser.add_argument('-i', '--interval', type=int, default=1, help='Interval between messages')

    return parser.parse_args()


if __name__ == '__main__':

    args = parse()

    # Create Kafka producer client
    producer = KafkaProducer(bootstrap_servers=args.brokers)

    # Start a counter to be used as the value of each test message
    val = 1

    try:

        while True:
            # Encode to UTF-8
            encoded_val = str(val).encode('utf-8')

            # Produce message
            print('Producing message to {}: "{}"'.format(args.topic, val))
            producer.send(args.topic, value=encoded_val)

            # Increment value for the next message we produce
            val += 1
            time.sleep(args.interval)

    except KeyboardInterrupt:
        producer.close()
