# PG CPU applet for MATE

## CPU applet to show all processor thread's load in a bar format

 Install:

sudo install.sh should put all the data in the appropriate directories.

This installer will also kill the old instance .. useful for development

  Usage:

 * Goto panel menu, click on  "Add to Panel"
 * Click on: "PG CPU Load Display"

 The python code can emit debug / status statements into syslog. To view them,
open a new terminal and run:

   sudo tail -f /var/log/syslog

See the source for examples of how to emit syslog statements from the panel applet;

Notables:

  This python project is a good platform for MATE applet development, as the
  project contains all the elements for install / code / run / un install cycle

  This project shows how to populate multiple instances of Applets / Widgets
  from the GLib timer.

  Python is an ideal platform for this kind of task ...

sudo remove.sh should erase all traces of this project from the system

### Small picture of the CPU Load Indicator:

![Image](pgcpu.jpg)

PG