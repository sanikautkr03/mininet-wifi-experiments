from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def custom_topology():
    # Create a network with 1 remote controller, 3 switches, and 6 hosts.
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)  # Using OVSKernelSwitch
    
    # Add Remote Controller
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Add Switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Add Hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')

    # Connect Hosts to Switches
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(h5, s3)
    net.addLink(h6, s3)

    # Connect Switches (create redundant paths)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s1)

    # Start the network
    net.start()

    # Enable Spanning Tree Protocol to avoid loops
    print("*** Enabling STP on switches...")
    for sw in net.switches:
        sw.cmd('ovs-vsctl set Bridge', sw.name, 'stp_enable=true')

    # Print message for waiting
    print("\n*** Waiting for STP to converge (approx 30 seconds)...")
    print("*** Mininet CLI started. Type 'exit' to stop the network.\n")
    CLI(net)

    # Stop the network
    net.stop()


if __name__ == '__main__':  # Corrected line
    setLogLevel('info')  # Set Mininet logging level to INFO
    custom_topology()
