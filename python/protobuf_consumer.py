#!/usr/bin/env python
# Reference: https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/protobuf_consumer.py
#
# This is a simple example of the DeserializingConsumer using protobuf.
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
#
import argparse

# Protobuf generated class; resides at ./user_pb2.py
import user_pb2
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import StringDeserializer


def main(args):
  topic = args.topic

  protobuf_deserializer = ProtobufDeserializer(user_pb2.User)
  string_deserializer = StringDeserializer('utf_8')

  consumer_conf = {'bootstrap.servers': args.bootstrap_servers,
                   'key.deserializer': string_deserializer,
                   'value.deserializer': protobuf_deserializer,
                   'group.id': args.group,
                   'auto.offset.reset': "earliest"}

  consumer = DeserializingConsumer(consumer_conf)
  consumer.subscribe([topic])

  while True:
    try:
      # SIGINT can't be handled when polling, limit timeout to 1 second.
      msg = consumer.poll(1.0)
      if msg is None:
        continue

      user = msg.value()
      if user is not None:
        print("User record {}:\n"
              "\tname: {}\n"
              "\tfavorite_number: {}\n"
              "\tfavorite_color: {}\n"
              .format(msg.key(), user.name,
                      user.favorite_color,
                      user.favorite_number))
    except KeyboardInterrupt:
      break

  consumer.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="ProtobufDeserializingConsumer Example")
  parser.add_argument('-b', dest="bootstrap_servers", required=True,
                      help="Bootstrap broker(s) (host[:port])")
  parser.add_argument('-s', dest="schema_registry", required=True,
                      help="Schema Registry (http(s)://host[:port]")
  parser.add_argument('-t', dest="topic", default="_kafkaclient-pythonexample_protobuf",
                      help="Topic name")
  parser.add_argument('-g', dest="group", default="pythonexample_protobuf",
                      help="Consumer group")

  main(parser.parse_args())
