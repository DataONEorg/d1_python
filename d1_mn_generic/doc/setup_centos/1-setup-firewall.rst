CentOS 7.3 Firewall Setup
=========================



Install firewalld
~~~~~~~~~~~~~~~~~

GMN will require ports 80 and 443 to be opened. So after logging in to your server as a user with sudoer privileges, the first step is to get the firewall
 setup. We begin by ensuring that the firewall management package is installed on your server and started.


**Update yum.**::

    $ sudo yum -y update


**Install firewalld**::

	$ sudo yum install firewalld
	$ sudo systemctl unmask firewalld
	$ sudo systemctl start firewalld




Configure Firewall with Network Interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next we want to achieve the binding of network interfaces to firewalld zones. This example uses the default public zone. First we need to identify your network interfaces.::

	$ ifconfig -a


The interfaces described in response will look something like this::

	eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 138.197.100.216  netmask 255.255.240.0  broadcast 138.197.111.255
        inet6 fe80::3c64:d3ff:fe95:187b  prefixlen 64  scopeid 0x20<link>
        ether 3e:64:d3:95:18:7b  txqueuelen 1000  (Ethernet)
        RX packets 467254  bytes 268127560 (255.7 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 335825  bytes 72203530 (68.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

    eth1: flags=4098<BROADCAST,MULTICAST>  mtu 1500
        ether f2:ac:61:7b:73:10  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

    lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 81687  bytes 26998580 (25.7 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 81687  bytes 26998580 (25.7 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0



There should be one or more network interfaces available, such as "eth0" or
"eth1". Ignore an entry such as *“LOOPBACK,RUNNING”*.The firewall management system we are using binds these network interfaces to something called a “zone”. There is the potential for multiple zones which can have different configuration options, but we aren’t going to worry about that here. We just need t he simplest configuration using the default zone. The
*public zone* will be the default. So at this point we will check whether or not the network interfaces we identified with “ifconfig -a” are bound to the public zone. We can check that with this command::

	$ sudo firewall-cmd --zone=public --list-all


Which return::

  public (active)
    target: default
    icmp-block-inversion: no
    interfaces:
    sources:
    services: dhcpv6-client http https ssh
    ports: 443/tcp
    protocols:
    masquerade: no
    forward-ports:
    sourceports:
    icmp-blocks:
    rich rules:


If the space next to the “interfaces” line contains the network interfaces, such as eth0 and eth1 in this example, then they are already bound to the public zone. However, if that line is empty, you will need to bind your network interfaces to the firewall zone as follows.



**Bind Network Interfaces to Zone**::

  $ sudo firewall-cmd --permanent --zone=public --change-interface=eth0
  $ sudo firewall-cmd --permanent --zone=public --change-interface=eth1
  $ sudo firewall-cmd --reload


Substituting the names of your interfaces in ``--change-interface=``. Now, when you enter the command::

  $ sudo firewall-cmd --zone=public --list-all

The network interfaces should be listed::

  public (active)
    target: default
    icmp-block-inversion: no
    interfaces: eth0 eth1
    sources:
    services: dhcpv6-client ssh
    ports:
    protocols:
    masquerade: no
    forward-ports:
    sourceports:
    icmp-blocks:
    rich rules:


Another way to confirm that everything is as it should be is to use this command::

  $ firewall-cmd --get-active-zones


Which will return output similar to::

  public
    interfaces: eth1 eth0

Open HTTP & HTTPS Ports
~~~~~~~~~~~~~~~~~~~~~~~


Now we can specify rules for handling specific ports and services, using the below commands.::

  $ sudo firewall-cmd --permanent --add-service=http
  $ sudo firewall-cmd --permanent --add-service=https
  $ sudo firewall-cmd --permanent --add-port=80/tcp
  $ sudo firewall-cmd --permanent --add-port=443/tcp
  $ sudo firewall-cmd --reload

  $ sudo systemctl enable firewalld

