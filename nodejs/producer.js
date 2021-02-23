'use strict';
const { Kafka } = require('kafkajs')
const { SchemaRegistry, readAVSCAsync } = require('@kafkajs/confluent-schema-registry')
const faker = require('faker')


const kafka = new Kafka({
  clientId: 'my-app',
  brokers: [process.env.BROKERS]
})

const producer = kafka.producer()

const registry = new SchemaRegistry({ host: process.env.SCHEMA_REGISTRY_URL })

async function send_message() {
  await producer.connect()

  const schema = await readAVSCAsync('schemas/person.avsc')
  const { id } = await registry.register(schema)

  const msgValue = { "full_name": faker.name.findName() }

  const outgoingMessage = {
    value: await registry.encode(id,msgValue)
  }

  await producer.send({
    topic: process.env.TOPIC,
    messages: [
      outgoingMessage
    ],
  })
  await producer.disconnect()
}

send_message().catch(console.error)
