#! /usr/local/bin/python3

# Consume and display messages from a Kafka topic

import argparse

from kafka import KafkaConsumer


def parse():
    """Parse command line"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--brokers', default='kafka:9092', help='Kafka bootstrap brokers')
    parser.add_argument('-t', '--topic', default='test-topic', help='Name of topic to consume from')

    return parser.parse_args()


if __name__ == '__main__':

    args = parse()

    # Create Kafka consumer client
    consumer = KafkaConsumer(bootstrap_servers=args.brokers)

    # Subscribe to topic
    print('Subscribing to topic {}'.format(args.topic))
    consumer.subscribe(args.topic)

    try:

        # Poll the topic for new messages
        for msg in consumer:

            # Decode the value for display
            decoded_val = msg.value.decode('utf-8')
            # Display the value of the message that was consumed
            print('Consumed message from {}: "{}"'.format(args.topic, decoded_val))

    except KeyboardInterrupt:
        consumer.close()
