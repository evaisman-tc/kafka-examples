'use strict';
const { Kafka } = require('kafkajs')
const { SchemaRegistry } = require('@kafkajs/confluent-schema-registry')

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: [process.env.BROKERS]
})

const registry = new SchemaRegistry({ host: process.env.SCHEMA_REGISTRY_URL })

const consumer = kafka.consumer({ groupId: 'test-group' })

async function receive_messages() {
  await consumer.connect()
  await consumer.subscribe({ topic: 'test-topic2', fromBeginning: true })

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const decodedValue = await registry.decode(message.value)
      console.log(decodedValue)
    },
  })
}

receive_messages().catch(console.error) 