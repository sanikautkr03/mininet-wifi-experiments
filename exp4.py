#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.topo import Topo
from time import sleep

class WebTopo(Topo):
    def build(self):
        # Add two hosts and one switch
        h1 = self.addHost('h1')  # Web server
        h2 = self.addHost('h2')  # Client
        s1 = self.addSwitch('s1')

        # Create links between hosts and switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)

if __name__ == '__main__':
    # Create network with RemoteController
    topo = WebTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    print("*** Starting network")
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    print("*** Configuring web server")

    # Create a basic HTML page
    html_content = "<html><body><h1>Hello from Mininet Web Server!</h1></body></html>"
    h1.cmd("mkdir -p /tmp/webserver")
    h1.cmd(f"echo '{html_content}' > /tmp/webserver/index.html")

    # Start the web server on h1
    h1.cmd("cd /tmp/webserver && python3 -m http.server 80 &")
    sleep(2)  # Give time for the server to start

    print("*** Web server running on h1. Client fetching the page...\n")

    # Use h2 to fetch the web page from h1
    result = h2.cmd("curl http://10.0.0.1")
    print("=== Client (h2) received ===\n")
    print(result)

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()
