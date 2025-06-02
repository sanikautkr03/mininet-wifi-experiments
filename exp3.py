#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI

def testConnectivity():
    print("*** Creating network")
    
    # Create a Mininet object with no controller initially
    net = Mininet(controller=None, link=TCLink)

    # Add a remote controller that connects to the remote controller at IP 127.0.0.1, port 6633
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    print("*** Adding switch")
    s1 = net.addSwitch('s1')

    print("*** Adding hosts")
    h1 = net.addHost('h1', ip='10.0.0.1/8')
    h2 = net.addHost('h2', ip='10.0.0.2/8')
    h3 = net.addHost('h3', ip='10.0.0.3/8')
    h4 = net.addHost('h4', ip='10.0.0.4/8')

    print("*** Creating links")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    print("*** Starting network")
    net.start()

    print("\n*** Testing connectivity between all host pairs\n")
    hosts = [h1, h2, h3, h4]

    for i in range(len(hosts)):
        for j in range(i+1, len(hosts)):
            src = hosts[i]
            dst = hosts[j]
            print(f"--- {src.name} -> {dst.name} ---")
            result = src.cmd(f'ping -c 2 {dst.IP()}')
            print(result)

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testConnectivity()
