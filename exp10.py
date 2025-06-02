#!/usr/bin/python3

from mininet.node import RemoteController, Host
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.log import setLogLevel, info
import time

def topology():
    net = Mininet_wifi(controller=RemoteController, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating mobile stations\n")
    sta1 = net.addStation('sta1', position='10,20,0')
    sta2 = net.addStation('sta2', position='15,25,0')
    sta3 = net.addStation('sta3', position='20,20,0')
    sta4 = net.addStation('sta4', position='25,25,0')

    info("*** Creating AP\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='50,50,0')

    info("*** Creating Web Server Host\n")
    h1 = net.addHost('h1', ip='10.0.0.100')

    info("*** Adding Controller\n")
    c0 = net.addController('c0', controller=RemoteController)

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Setting mobility\n")
    net.setMobilityModel(time=0, model='RandomWalk', max_x=100, max_y=100, min_v=1, max_v=3)

    info("*** Creating links\n")
    net.addLink(ap1, h1)  # Wired link to server

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])

    info("*** Starting simple HTTP server on h1\n")
    h1.cmd('python3 -m http.server 80 > webserver.log 2>&1 &')

    info("*** Letting network stabilize\n")
    time.sleep(5)

    info("*** Simulating client load\n")
    for sta in [sta1, sta2, sta3, sta4]:
        sta.cmd('curl http://10.0.0.100 > /dev/null 2>&1 &')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
