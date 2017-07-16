import os
import datetime
import uuid
import logging
from time import sleep
import gevent
from gevent.wsgi import WSGIServer
from flask import Flask, jsonify

from kazoo.client import KazooClient, EventType
from kazoo.exceptions import NodeExistsException, NoNodeException

logging.basicConfig()

zoo_hosts = os.getenv('ZK_HOSTS')
zk = KazooClient(hosts=zoo_hosts)
zk.start()

identity = uuid.uuid4().hex
lease = zk.NonBlockingLease(
    "/welcome", datetime.timedelta(minutes=1),
    identifier=identity
)
if lease:
    print(f"Welcome")


class LeaderElection(object):

    def __init__(self):
        self.identity = bytes(uuid.uuid4().hex, encoding='utf')
        self.leader = None
        self.election = None

    @property
    def is_leader(self):
        return self.leader == self.identity

    def elected(self, election):
        try:
            zk.create('/leader', self.identity, ephemeral=True)
            print("I'm a leader")
        except NodeExistsException:
            pass

    def new_election(self):
        self.election = zk.Election("/election", self.identity)
        self.election.run(self.elected, election)

    def run_elect(self):
        @zk.DataWatch("/leader")
        def watch_leader(data, stat):
            if data:
                self.leader = data
                if self.election:
                    self.election.cancel()
            else:
                self.new_election()


app = Flask(__name__)


@app.route('/')
def welcome():
    return jsonify(
        title='Hello',
        leader=election.leader and str(election.leader, encoding='utf'),
        is_leader=election.is_leader
    )


election = LeaderElection()
gevent.spawn(election.run_elect)
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
