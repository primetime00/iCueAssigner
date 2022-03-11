from modules.network.server import Server
from modules.network.pipe_server import PipeServer
import modules.network.client as client
import modules.network.com_client as com_client

server = Server()
pipe_servers = {}
Client = client.Client
ClientData = client.ClientData
ComClient = com_client.ComClient

def GetPipeServer(name):
    if name not in pipe_servers:
        pipe_servers[name] = PipeServer(name)
        pipe_servers[name].start()
    return pipe_servers[name]


