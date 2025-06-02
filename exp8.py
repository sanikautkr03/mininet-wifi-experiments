#!/usr/bin/python3

from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP, Station
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.node import RemoteController
from mininet.log import setLogLevel, info

def topology():
    net = Mininet_wifi(controller=RemoteController,
                       link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating stations\n")
    sta1 = net.addStation('sta1', position='5,30,0')
    sta2 = net.addStation('sta2', position='5,35,0')

    info("*** Creating access points\n")
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='10,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='40,30,0')

    info("*** Adding controller\n")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Defining mobility\n")
    net.mobility(sta1, 'start', time=1, position='5,30,0')
    net.mobility(sta1, 'stop', time=20, position='45,30,0')  # Moves from ap1 to ap2

    net.mobility(sta2, 'start', time=1, position='5,35,0')
    net.mobility(sta2, 'stop', time=20, position='45,35,0')  # Also roams

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    info("*** Optional: Start packet capture\n")
    sta1.cmd('tcpdump -i sta1-wlan0 -w sta1.pcap &')
    sta2.cmd('tcpdump -i sta2-wlan0 -w sta2.pcap &')
    ap1.cmd('tcpdump -i ap1-wlan1 -w ap1.pcap &')
    ap2.cmd('tcpdump -i ap2-wlan1 -w ap2.pcap &')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
