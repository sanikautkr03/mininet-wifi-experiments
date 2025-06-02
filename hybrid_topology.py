#!/usr/bin/python3

from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.node import RemoteController
from mininet.log import setLogLevel, info

def topology():
    net = Mininet_wifi(controller=RemoteController,
                       link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    # Wireless stations with positions and IPs
    sta1 = net.addStation('sta1', ip='10.0.0.1/24', position='10,30,0')
    sta2 = net.addStation('sta2', ip='10.0.0.2/24', position='20,30,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3/24', position='30,30,0')
    # Added sta4 with IP 10.0.0.6 to fix unreachable ping issue
    sta4 = net.addStation('sta4', ip='10.0.0.6/24', position='40,30,0')

    # Wired hosts
    h1 = net.addHost('h1', ip='10.0.1.1/24')
    h2 = net.addHost('h2', ip='10.0.1.2/24')

    # Access point, switches and router
    ap1 = net.addAccessPoint('ap1', ssid='office-wifi', mode='g', channel='1',
                             position='20,50,0')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Router host with interfaces in both subnets
    router = net.addHost('r0')

    # Remote controller
    c0 = net.addController('c0', controller=RemoteController,
                           ip='127.0.0.1', port=6633)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    # Bridge wlan0 to AP datapath to connect wireless subnet to switch
    ap1.cmd('ovs-vsctl add-port ap1 wlan0')

    info("*** Creating links\n")
    net.addLink(ap1, s1)
    net.addLink(s1, router)
    net.addLink(router, s2)
    net.addLink(s2, h1)
    net.addLink(s2, h2)

    info("*** Starting network\n")
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])
    ap1.start([c0])

    info("*** Configuring Router\n")
    # Assign IPs to router interfaces
    router.cmd('ifconfig r0-eth0 10.0.0.254/24')
    router.cmd('ifconfig r0-eth1 10.0.1.254/24')
    router.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Set gateways for wireless stations including sta4
    for sta in [sta1, sta2, sta3, sta4]:
        sta.cmd('ip route add default via 10.0.0.254')

    # Set gateways for wired hosts
    for host in [h1, h2]:
        host.cmd('ip route add default via 10.0.1.254')

    info("*** Configuring QoS using tc\n")
    h1.cmd("tc qdisc add dev h1-eth0 root tbf rate 2mbit burst 32kbit latency 400ms")
    h2.cmd("tc qdisc add dev h2-eth0 root tbf rate 1mbit burst 32kbit latency 500ms")
    sta1.cmd("tc qdisc add dev sta1-wlan0 root tbf rate 3mbit burst 32kbit latency 300ms")

    info("*** Adding ACL (blocking sta3 ping to h2)\n")
    # Blocking ICMP from sta3 (10.0.0.3) to h2
    h2.cmd("iptables -A INPUT -s 10.0.0.3 -p icmp -j DROP")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
