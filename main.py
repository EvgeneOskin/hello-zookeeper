import os
import logging
from kazoo.client import KazooClient


logging.basicConfig()

zoo_hosts = os.getenv('ZK_HOSTS')
zk = KazooClient(hosts=zoo_hosts)
zk.start()

counter = zk.Counter("/connected")
counter += 1
print(f"There were ${counter.value} connections")

barrier = zk.DoubleBarrier('/entrance', num_clients=3)

barrier.enter()

election = zk.Election("/welcome")


def welcome():
    workers_number = len(election.contenders())
    print("Cluster is up and running with ${workers_number}")


election.run(welcome)

barrier.leave()
