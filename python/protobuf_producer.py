#!/usr/bin/env python
# Reference: https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/protobuf_producer.py
#
# This is a simple example of the SerializingProducer using Protobuf.
#
# To regenerate Protobuf classes you must first install the protobuf
# compiler. Once installed you may call protoc directly or use make.
#
# See the protocol buffer docs for instructions on installing and using protoc.
# https://developers.google.com/protocol-buffers/docs/pythontutorial
#
# After installing protoc execute the following command from the examples
# directory to regenerate the user_pb2 module.
# `make`

import argparse
import time
from uuid import uuid4

# Protobuf generated class; resides at ./user_pb2.py
import user_pb2
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from faker import Faker


def delivery_report(err, msg):
  """
  Reports the failure or success of a message delivery.

  Args:
      err (KafkaError): The error that occurred on None on success.

      msg (Message): The message that was produced or failed.

  Note:
      In the delivery report callback the Message.key() and Message.value()
      will be the binary format as encoded by any configured Serializers and
      not the same object that was passed to produce().
      If you wish to pass the original object(s) for key and value to delivery
      report callback we recommend a bound callback or lambda where you pass
      the objects along.

  """
  if err is not None:
    print("Delivery failed for User record {}: {}".format(msg.key(), err))
    return
  print('User record {} successfully produced to {} [{}] at offset {}'.format(
      msg.key(), msg.topic(), msg.partition(), msg.offset()))


def main(args):
  topic = args.topic
  fake = Faker()
  schema_registry_conf = {'url': args.schema_registry}
  schema_registry_client = SchemaRegistryClient(schema_registry_conf)

  protobuf_serializer = ProtobufSerializer(user_pb2.User,
                                           schema_registry_client)

  producer_conf = {'bootstrap.servers': args.bootstrap_servers,
                   'key.serializer': StringSerializer('utf_8'),
                   'value.serializer': protobuf_serializer}

  producer = SerializingProducer(producer_conf)

  print("Producing user records to topic {}. ^C to exit.".format(topic))
  try:
    while True:
      # Serve on_delivery callbacks from previous calls to produce()
      producer.poll(0.0)
      user_name = fake.name()
      user_favorite_number = fake.pyint()
      user_favorite_color = fake.color_name()
      user = user_pb2.User(name=user_name,
                           favorite_color=user_favorite_color,
                           favorite_number=user_favorite_number)
      producer.produce(topic=topic, key=str(uuid4()), value=user,
                       on_delivery=delivery_report)
      time.sleep(1)
  except KeyboardInterrupt:
    print("Interrupted!")
  print("\nFlushing records...")
  producer.flush()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description="ProtobufSerializingProducer Example")
  parser.add_argument('-b', dest="bootstrap_servers", required=True,
                      help="Bootstrap broker(s) (host[:port])")
  parser.add_argument('-s', dest="schema_registry", required=True,
                      help="Schema Registry (http(s)://host[:port]")
  parser.add_argument('-t', dest="topic", default="_kafkaclient-pythonexample_protobuf",
                      help="Topic name")

  main(parser.parse_args())
