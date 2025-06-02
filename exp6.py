from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import Station, OVSKernelAP

def topology():
    net = Mininet_wifi(controller=RemoteController, link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='10,30,0')
    sta2 = net.addStation('sta2', position='20,30,0')
    sta3 = net.addStation('sta3', position='30,30,0')
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g',
                             channel='1', position='15,50,0', range=50)
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g',
                             channel='6', position='35,50,0', range=50)
    c1 = net.addController('c1', controller=RemoteController,
                           ip='127.0.0.1', port=6633)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
