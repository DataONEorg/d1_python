The Member Node Stress Tester is a system that generates synthetic queries for
Member Nodes. It can load test DataONE Member Node APIs such as
`MNCore.getLogRecords()`, `MNRead.listObjects()` and `MNStorage.create()`.

.. graphviz::

  digraph A {
    dpi=72;
    "DataONE Common" -> "DataONE Client" -> "Stress Tester"
    "DataONE Common" -> "Stress Tester"
    "Instance Generator" -> "Stress Tester"
    "Test Utilities" -> "Stress Tester"
    "Multi-Mechanize" -> "Stress Tester"
  }

