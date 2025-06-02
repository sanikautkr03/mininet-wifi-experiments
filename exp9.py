#!/usr/bin/python3

from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from time import sleep

def handover(station, ap1, ap2, threshold=-70):
    """ Check RSSI and trigger handover if below threshold """
    while True:
        # Get RSSI from AP1 (current AP)
        rssi_ap1 = station.get_rssi(ap1)
        rssi_ap2 = station.get_rssi(ap2)

        if rssi_ap1 is not None:
            info(f"\n{station.name} RSSI from {ap1.name}: {rssi_ap1} dBm\n")

        if rssi_ap1 is not None and rssi_ap1 < threshold and rssi_ap2 is not None and rssi_ap2 > rssi_ap1:
            info(f"\n{station.name} is handing over from {ap1.name} to {ap2.name}\n")
            station.cmd(f"iw dev {station.params['wlan'][0]} disconnect")
            station.cmd(f"iw dev {station.params['wlan'][0]} connect {ap2.ssid}")
            break

        sleep(2)

def topology():
    net = Mininet_wifi(controller=RemoteController,
                       link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating stations\n")
    sta1 = net.addStation('sta1', position='5,30,0')
    sta2 = net.addStation('sta2', position='5,40,0')

    info("*** Creating access points\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='10,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6', position='50,30,0')

    info("*** Adding controller\n")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Mobility configuration\n")
    net.mobility(sta1, 'start', time=1, position='5,30,0')
    net.mobility(sta1, 'stop', time=15, position='55,30,0')

    net.mobility(sta2, 'start', time=1, position='5,40,0')
    net.mobility(sta2, 'stop', time=15, position='55,40,0')

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    info("*** Starting ping test\n")
    sta1.cmd('ping -c5 10.0.0.2 &')

    info("*** Running handover logic for sta1\n")
    net.get('sta1').cmd('iw dev sta1-wlan0 connect ssid-ap1')  # Initial connection
    sleep(3)  # Let initial connection settle

    # Start RSSI monitoring and handover
    handover_thread_sta1 = net.get('sta1').popen(['python3', '-c', f'''
import time
from mininet.log import info
from subprocess import check_output

def get_rssi(ap_mac):
    try:
        result = check_output("iw sta1-wlan0 link", shell=True).decode()
        if "signal:" in result:
            rssi = int(result.split("signal:")[1].split(" dBm")[0].strip())
            return rssi
    except:
        return None

while True:
    rssi = get_rssi("{ap1.MAC()}")
    if rssi is not None and rssi < -70:
        info("RSSI low. Disconnecting and reconnecting to AP2\\n")
        _ = check_output("iw dev sta1-wlan0 disconnect", shell=True)
        time.sleep(1)
        _ = check_output("iw dev sta1-wlan0 connect ssid-ap2", shell=True)
        break
    time.sleep(2)
    '''])

    info("*** CLI for further testing\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
