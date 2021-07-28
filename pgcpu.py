#!/usr/bin/env python

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import sys, time, os, random, syslog

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('MatePanelApplet', '4.0')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import MatePanelApplet

inst_arr     = []
was_inst    = 0

class vertbar(Gtk.DrawingArea):

    def __init__(self, ww, hh, barcolor):
        Gtk.DrawingArea.__init__(self)
        self.set_can_focus(True)
        self.connect("draw", self.draw_event)
        self.set_size_request(ww, hh)
        self.barcolor = barcolor
        self.cent = 10

    def set_procent(self, cent):
        if cent > 100: cent = 100
        if cent < 1: cent = 1

        self.cent = cent
        self.queue_draw()

    def draw_event(self, pdoc, cr):
        rect = self.get_allocation()
        if rect.height < 0:
            return

        cr.set_source_rgba(*self.barcolor)
        cr.rectangle( 1, 2, rect.width-2, rect.height-4)
        cr.fill()

        hhh = rect.height - (self.cent * rect.height-4) // 100
        #print("draw", hhh)

        cr.set_source_rgba(0., 1., 0.)
        cr.rectangle( 1, hhh, rect.width-2, rect.height)
        cr.fill()

def apply_screen_coord_correction(self, x, y, widget, relative_widget):

    corrected_y = y; corrected_x = x
    rect = widget.get_allocation()
    screen_w = Gdk.Screen.width()
    screen_h = Gdk.Screen.height()
    delta_x = screen_w - (x + rect.width)
    delta_y = screen_h - (y + rect.height)
    if delta_x < 0:
        corrected_x += delta_x
    if corrected_x < 0:
        corrected_x = 0
    if delta_y < 0:
        corrected_y = y - rect.height - relative_widget.get_allocation().height
    if corrected_y < 0:
        corrected_y = 0
    return [corrected_x, corrected_y]


def show_dialog(widget, event=None):

    win = Gtk.Window()
    win.connect('destroy', Gtk.main_quit)
    win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    hbox = Gtk.VBox()
    hbox.pack_start(Gtk.Label(" "), 1,1,2)
    lab = Gtk.Label("       PG CPU Load Display App        ")
    hbox.pack_start(lab, 1,1,2)
    hbox.pack_start(Gtk.Label(" "), 1,1,2)

    lab2 = Gtk.Label("       Written by Peter Glen        ")
    hbox.pack_start(lab2, 1,1,2)
    hbox.pack_start(Gtk.Label(" "), 1,1,2)

    win.add(hbox)
    win.show_all()
    Gtk.main()


def show_msg(widget, msg="Empty Message", event=None):

    win = Gtk.Window()
    win.connect('destroy', Gtk.main_quit)
    win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    hbox = Gtk.VBox()
    hbox.pack_start(Gtk.Label(" "), 1,1,2)
    lab = Gtk.Label(msg)
    hbox.pack_start(lab, 1,1,2)
    hbox.pack_start(Gtk.Label(" "), 1,1,2)

    lab2 = Gtk.Label("       Written by Peter Glen        ")
    hbox.pack_start(lab2, 1,1,2)
    hbox.pack_start(Gtk.Label(" "), 1,1,2)

    win.add(hbox)
    win.show_all()
    Gtk.main()

def add_timer(widget, event=None):
    win = Gtk.Window()
    win.connect('destroy', Gtk.main_quit)
    win.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    win.show_all()
    Gtk.main()

def append_menu(applet):

    menu_xml="""
        <menuitem item="Item 1" action="AboutAction"/>
    """
    #    <menuitem item="Item 2" action="TimerAction"/>
    #    <menuitem item="Item 3" action="QuitAction"/>

    actions = [
        ('AboutAction', None, 'About CPU Applet', None, None, show_dialog),
       # ('TimerAction', None, 'Add Timer', None, None, add_timer),
       # ('QuitAction', None, 'Quit Applet', None, None, Gtk.main_quit),
    ]

    action_group = Gtk.ActionGroup.new("Timer")
    action_group.add_actions(actions, applet)
    applet.setup_menu(menu_xml, action_group)


def applet_fill(applet):

    #print("Fill applet")

    # you can use this path with gio/gsettings
    settings_path = applet.get_preferences_path()

    #print("settings_path", settings_path)

    box = Gtk.Box()

    #try:
    #   pixbuf = Gtk.IconTheme.get_default().load_icon("document-new", applet.get_size() / 4, 0)
    #   button_icon = Gtk.Image.new_from_pixbuf(pixbuf)
    #except:
    #    print("icon", sys.exc_info())
    #    button_icon = Gtk.Label("Icons")
    #box.add(button_icon)

    #label = Gtk.Label(label="Timer")
    #box.add(label)

    applet.cpuarr       = []
    applet.old_total    = []
    applet.old_idle     = []

    for aa in range(os.cpu_count()):
        barcolor = [.6, .6, .6]
        vb = vertbar(6, applet.get_size(), barcolor)
        applet.cpuarr.append(vb)
        box.add(vb)
        applet.old_total.append(0); applet.old_idle.append(0)

    #button = Gtk.Button(label="QUIT")
    #button.connect('clicked', Gtk.main_quit)
    #box.add(button)
    box.add(Gtk.Label(" "))

    applet.add(box)
    applet.show_all()
    append_menu(applet)


def  timex():

    global inst_arr

    #print("timer fired", time.ctime())
    #syslog.syslog("timer fired %d %s" % (os.getpid(), time.ctime()))
    #syslog.syslog("inst_arr %s" % str(inst_arr))

    try:
        for aa in inst_arr:
            if aa:
                proc_one(aa.cpuarr, aa.old_total, aa.old_idle)
    except:
        pass

    #  Restart no matter what
    GLib.timeout_add(1000, timex)

# ------------------------------------------------------------------------

def proc_one(cpuarr, old_total, old_idle):

    try:
        fp = open("/proc/stat")
        sss = fp.read()
        fp.close()

        #print("sss", sss)

        #      0        1     2      3       4       5
        #              user  nice  system  idle     i/o
        #b2 ['cpu15', 19147, 8,    4862,   1382562, 1133, 0, 6, 0, 0, 0]

        #print("      ", end = "")
        cnt = 0; cnt2 = 0
        for aa in str.split(sss, "\n"):
            if "cpu" in aa:
                if cnt:
                    bb = aa.split()
                    for cc in range(len(bb)):
                        try:
                            bb[cc] = int(bb[cc])
                        except:
                            pass

                    #print("bb2", bb)

                    total  = bb[1] + bb[2] + bb[3] + bb[4]
                    idle   = bb[2] + bb[4]

                    ttt =  total - old_total[cnt2];
                    iii =  idle - old_idle[cnt2];

                    #print("ttt", ttt, "iii", iii, end= "" )

                    old_total[cnt2] = total;
                    old_idle[cnt2]  = idle;

                    ccc = 0;
                    try:
                        ccc = 100 - (iii  /  ttt) * 100
                    except:
                        pass

                    #print("  %.2f " % ccc, end = " " )
                    #cpuarr[cnt -1 ].set_procent(random.random() * 100)
                    cpuarr[cnt-1 ].set_procent(ccc)
                    cnt2 += 1

            cnt += 1
    except:
        #print("exc", sys.exc_info())
        syslog.syslog("exce %s" % sys.exc_info())


# Substract current process from display

def destr(obj, instance):
    global inst_arr
    #syslog.syslog("Factory applet destroyed %d" % instance)
    inst_arr[instance] = 0
    #syslog.syslog("inst_arr %s" % str(inst_arr))

# ------------------------------------------------------------------------
# Entry point

def applet_factory(applet, iid, data):

    #syslog.syslog("Factory applet %s" % iid)

    if iid != "pgcpu":
       return False

    global  was_inst, inst_arr

    applet_fill(applet)

    #syslog.syslog("Started applet %d %s" % (os.getpid(), time.ctime()))

    applet.connect("destroy", destr, was_inst)

    was_inst += 1
    inst_arr.append(applet)

    #print("Started timer")
    GLib.timeout_add(1000, timex)
    return True

#print(dir(MatePanelApplet.Applet))

MatePanelApplet.Applet.factory_main("pgcpuFactory", True,
                                    MatePanelApplet.Applet.__gtype__,
                                    applet_factory, None)

# EOF
