from mycroft_bus_client import MessageBusClient, Message

client = MessageBusClient()

def ready(message: Message):
    print("ready")
    print(message)

def not_paired(message: Message):
    print("not paired")
    print(message)

def paired(message: Message):
    print("paired")
    print(message)

def config_updated(message: Message):
    print("config updated")
    print(message)

client.on("mycroft.ready", ready)
client.on("mycroft.not.paired", not_paired)
client.on("mycroft.paired", paired)
client.on("configuration.updated", config_updated)

client.run_forever()