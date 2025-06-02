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
    stations = []
    positions = ['10,10,0', '15,20,0', '20,10,0', '25,15,0', '30,20,0', '35,10,0']
    for i in range(6):
        sta = net.addStation(f'sta{i+1}', position=positions[i])
        stations.append(sta)

    info("*** Creating access points\n")
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='10,50,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='25,50,0')
    ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='11', position='40,50,0')

    info("*** Adding remote controller\n")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Setting mobility model\n")
    net.setMobilityModel(time=0, model='RandomWayPoint', max_x=50, max_y=50, min_v=1, max_v=3)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])

    info("*** Optional: Start packet capture (comment out if not needed)\n")
    for sta in stations:
        sta.cmd(f'tcpdump -i {sta.name}-wlan0 -w {sta.name}.pcap &')
    ap1.cmd('tcpdump -i ap1-wlan1 -w ap1.pcap &')
    ap2.cmd('tcpdump -i ap2-wlan1 -w ap2.pcap &')
    ap3.cmd('tcpdump -i ap3-wlan1 -w ap3.pcap &')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
