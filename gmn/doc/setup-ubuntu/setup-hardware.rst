Hardware requirements and configuration
=======================================

Setting up the hardware.

:term:`GMN` is installed on a physical or virtual machine. Network connectivity is arranged so that GMN can be reached from the DataONE :term:`CN`\ s and from
:term:`client`\ s. Typically, this means that GMN is set up to be globally accessible from the web.

GMN can be used in a mode where it provides a DataONE interface to data that is already available on the web. When used in this way, GMN must also have access to the web site which holds the data.

The requirements for RAM, CPU, disk and network resources are workload dependent. Below is benchmarks for two different setups.


Benchmarks
~~~~~~~~~~

To give an indication of the hardware that may be required for hosting GMN, some benchmarks are provided.

Configuration of benchmarking scripts:

- Concurrent calls per API: 5
- Science object size: 1024 bytes.
- Allow rules per object: 10
- listObjects / getLogRecords page size: 1000 objects


Hardware configuration 1
````````````````````````

================== =================================
**Machine type**   Physical
**CPU**            Intel Core2 Quad Q6600 @ 2.40GHz
**RAM**            4GiB
**Disk**           5400 RPM SATA (I/O @ 60 MiB/s)
================== =================================

===================================================================== ===========================
API                                                                   Transactions per second
===================================================================== ===========================
MNStorage.create()                                                    9.8
MNRead.get()                                                          35.3
MNRead.listObjects()                                                  0.5
MNCore.getLogRecords(), paged, called by CN                           0.36
MNCore.getLogRecords(), specific object, called by regular subject    40.6
Combination of MNStorage.create(), MNRead.get(), MNRead.listObjects() 4.4
Combination of MNCore.getLogRecords(), MNRead.get()                   36.2
===================================================================== ===========================


Hardware configuration 2
````````````````````````

================== =============================
**Machine type**   Virtual
**CPU**            Intel Xeon E7540 @ 2.00GHz
**RAM**            32GiB
**Disk**           NFS (I/O @ 45MiB/s)
================== =============================

===================================================================== ===========================
API                                                                   Transactions per second
===================================================================== ===========================
MNStorage.create()                                                    9.3
MNRead.get()                                                          5.6
MNRead.listObjects()                                                  0.35
MNCore.getLogRecords(), paged, called by CN                           0.2
MNCore.getLogRecords(), specific object, called by regular subject    6.0
Combination of MNStorage.create(), MNRead.get(), MNRead.listObjects() 2.8
Combination of MNCore.getLogRecords(), MNRead.get()                   5.24
===================================================================== ===========================

