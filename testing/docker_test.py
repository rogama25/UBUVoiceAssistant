import docker
client = docker.from_env()

myc = client.containers.get("mycroft")

print(myc)

out = myc.exec_run("./startup.sh")

print(out.output.decode("utf-8"))