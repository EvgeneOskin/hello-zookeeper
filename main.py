import os
import datetime
import uuid
import logging
from kazoo.client import KazooClient


logging.basicConfig()

zoo_hosts = os.getenv('ZK_HOSTS')
zk = KazooClient(hosts=zoo_hosts)
zk.start()

counter = zk.Counter("/connected")
counter += 1

min_nodes_number = int(os.getenv('MIN_NUMBER_OF_WORKERS'))
barrier = zk.DoubleBarrier('/entrance', min_nodes_number)

barrier.enter()

lease = zk.NonBlockingLease(
    "/welcome", datetime.timedelta(minutes=1),
    identifier="welcome " + uuid.uuid4().hex)

if lease:
    print(f"Welcome: There were ${counter.value} connections")


barrier.leave()
