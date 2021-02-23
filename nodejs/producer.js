const { Kafka } = require('kafkajs')
const { SchemaRegistry, readAVSCAsync } = require('@kafkajs/confluent-schema-registry')


const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
})

const producer = kafka.producer()

const registry = new SchemaRegistry({ host: 'http://localhost:8081' })

async function send_message() {
  await producer.connect()

  const schema = await readAVSCAsync('schemas/person.avsc')
  const { id } = await registry.register(schema)

  const msgValue = { "full_name": "test" }

  const outgoingMessage = {
    value: await registry.encode(id,msgValue)
  }

  await producer.send({
    topic: 'test-topic2',
    messages: [
      outgoingMessage
    ],
  })
  await producer.disconnect()
}

send_message().catch(console.error)
