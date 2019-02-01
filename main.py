#!/usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository  import Gtk, Gdk, Gio
import os
import sys
import subprocess
from gi.repository import GObject as gobject
import fcntl

dirname, filename = os.path.split(os.path.abspath(__file__))


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))



# MainWindow
class MainWindow(Gtk.Window):



    def __init__(self):
        Gtk.Window.__init__(self, title="aircrack-ng GUI")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)
        self.set_default_size(800,600)
        grid = Gtk.Grid()
        self.add(grid)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "aircrack-ng GUI"
        self.set_titlebar(hb)

        # Interfaces List
        command_interface = "/bin/iw dev | awk '$1==\"Interface\" {print $2}'"
        output_interface = os.popen(command_interface).read()
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        label_interface = Gtk.Label(label="Interfaces:")

        self.listbox = Gtk.ListBox()
        items = output_interface.split()
        for item in items:
            self.listbox.add(ListBoxRowWithData(item))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()

        def filter_func(row, data, notify_destroy):
            return False if row.data == 'Fail' else True

        self.listbox.set_sort_func(sort_func, None, False)
        self.listbox.set_filter_func(filter_func, None, False)
        self.selection_listbox=None

        def on_row_activated(listbox_widget, row):
            self.selection_listbox = row.data
            print(self.selection_listbox)
            return self.selection_listbox

        self.listbox.connect('row-activated', on_row_activated)
        box_outer.pack_start(self.listbox, True, True, 0)
        self.listbox.show_all()

        # Go to airmonwindow button
        button_airmon=Gtk.Button(label="airmon-ng")
        button_airmon.connect("clicked", self.whenbutton_airmon_clicked)

        # Go to scanWindow button
        button_scanWindow=Gtk.Button(label="Scan")
        button_scanWindow.connect("clicked", self.whenbutton_scanWindow_clicked)

        grid.add(label_interface)
        grid.add(box_outer)
        grid.attach(button_airmon, 0,4,1,1)
        grid.attach(button_scanWindow, 0,3,1,1)

    # airmonWindow button | functionality
    def whenbutton_airmon_clicked(self, button):
        if (self.selection_listbox is not None):
            interface=self.selection_listbox
            airmonWindow = AirmonWindow(interface)
            airmonWindow.show_all()
            self.hide()
        else: 
            def on_error_clicked(self):
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, "No interface is selected")
                dialog.format_secondary_text(
                    "Please make sure to select a valid interface")
                dialog.run()
                dialog.destroy()
            on_error_clicked(self)
        
    # scanWindow button | functionality
    def whenbutton_scanWindow_clicked(self, button):
        if (self.selection_listbox is not None):
            if ("mon" in self.selection_listbox):
                def on_error_clicked(self):
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                        Gtk.ButtonsType.OK, "Interface can't scan using iw with airmon-ng on")
                    dialog.format_secondary_text(
                        "Please stop airmon-ng and try again")
                    dialog.run()
                    dialog.destroy()
                on_error_clicked(self)
            else:
                interface=self.selection_listbox
                print(interface)
                scanwindow = scanWindow(interface)
                scanwindow.show_all()
                self.hide()
        else: 
            def on_error_clicked(self):
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, "No interface is selected")
                dialog.format_secondary_text(
                    "Please make sure to select a valid interface")
                dialog.run()
                dialog.destroy()
            on_error_clicked(self)
            
# AirmonWindow
class AirmonWindow(Gtk.Window):

    def __init__(self, interface):

        Gtk.Window.__init__(self, title="aircrack-ng GUI | airmon-ng")
        self.connect("destroy", Gtk.main_quit)
        grid = Gtk.Grid()

        # the scrolledwindow
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        # there is always the scrollbar (otherwise: AUTOMATIC - only if needed
        # - or NEVER)
        scrolled_window.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.add(scrolled_window)
        scrolled_window.add(grid)
        self.set_border_width(10)
        self.set_default_size(800,600)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "aircrack-ng GUI | airmon-ng"
        self.set_titlebar(hb)

        # airmon check & airmon check kill
        button_airmon_check = Gtk.Button(label="airmon-ng check")
        self.button_airmon_check_kill = Gtk.Button(label="airmon-ng check kill")
        self.button_airmon_check_kill.connect("clicked", self.whenbutton_airmon_check_kill_clicked, grid)
        button_airmon_check.connect("clicked", self.whenbutton_airmon_check_clicked, grid)

        #airmon start|stop {interface}
        button_airmon_start = Gtk.Button(label="airmon-ng start")
        button_airmon_start.connect("clicked", self.whenbutton_airmon_clicked, "start", interface)
        button_airmon_stop = Gtk.Button(label="airmon-ng stop")
        button_airmon_stop.connect("clicked", self.whenbutton_airmon_clicked, "stop", interface)

        # command log output
        self.label_commands_log = Gtk.Label(label='')
        self.ebox_airmon_commands_log = Gtk.EventBox()
        self.label_commands_log_output = Gtk.Label(label='')
        self.label_commands_log_output.set_selectable(True)
        self.label_commands_log_output.set_line_wrap_mode(True)
        self.ebox_airmon_commands_log.add(self.label_commands_log_output)


        # Systemd toggle
        self.label_systemd=Gtk.Label(label="\n In most cases, you need to stop your network manager service.\n If you are using systemd with NetworkManager.service you can stop it from here \n")
        self.button_systemd_start=Gtk.Button(label="Start NetworkManager.service")
        self.button_systemd_start.connect("clicked", self.whenbutton_systemd_clicked, "start")
        self.button_systemd_stop=Gtk.Button(label="Stop NetworkManager.service")
        self.button_systemd_stop.connect("clicked", self.whenbutton_systemd_clicked, "stop")
        label_systemd=Gtk.Label(label="\n Systemd Status: \n ")
        systemd_status=os.popen("gksudo /bin/systemctl status NetworkManager.service | awk '$1==\"Active:\" {print $0}'").read()
        self.label_systemd_status=Gtk.Label(systemd_status)

        # Go back to Main Window
        self.button_mainwindow=Gtk.Button(label="Go to Main Window")
        self.button_mainwindow.connect("clicked", self.Gotomainwindow)

        # grid
        grid.attach(self.button_mainwindow, 0, 1, 1, 1)
        grid.attach(button_airmon_check, 1, 1, 1, 1)
        grid.attach(button_airmon_start, 1, 4, 1, 1)
        grid.attach(button_airmon_stop, 1, 7, 1, 1)
        grid.attach(self.label_commands_log, 1,8,1,1)
        grid.attach(self.ebox_airmon_commands_log, 1, 10, 1, 1)
        grid.attach(self.label_systemd, 1, 15, 5, 5)
        grid.attach(self.button_systemd_start, 1, 20, 1,1)
        grid.attach(self.button_systemd_stop, 1, 22, 1,1)
        grid.attach(label_systemd, 1, 23, 1,1)
        grid.attach(self.label_systemd_status, 1, 24, 1,1)


    # airmon-ng (start|stop) button | functionality
    def whenbutton_airmon_clicked(self, button, arg, interface):
        if (arg=="start"):
            command_airmon_start= f"gksudo /bin/airmon-ng start {interface}"
            output_airmon_start = os.popen(command_airmon_start).read()
            self.label_commands_log_output.set_text(output_airmon_start)
            self.label_commands_log.set_text(f"airmon-ng start {interface} output:")
            return output_airmon_start
        elif (arg=="stop"):
            command_airmon_stop= f"gksudo /bin/airmon-ng stop {interface}"
            output_airmon_stop= os.popen(command_airmon_stop).read()
            self.label_commands_log_output.set_text(output_airmon_stop)
            self.label_commands_log.set_text(f"airmon-ng stop {interface} output:")
            return output_airmon_stop

    # airmon-ng check button | functionality
    def whenbutton_airmon_check_clicked(self, button, grid):
        def airmonCheck():
            command_airmon_check = "gksudo /bin/airmon-ng check"
            output_airmon_check = os.popen(command_airmon_check).read()
            return output_airmon_check

        self.label_commands_log_output.set_text(airmonCheck())
        self.label_commands_log.set_text("airmon-ng check output:")
        grid.attach(self.button_airmon_check_kill,3, 12, 1, 1)
        self.show_all()
        
    # airmon-ng check kill button | functionality
    def whenbutton_airmon_check_kill_clicked(self, button, grid):
        def airmonCheckKill():
            command_airmon_check_kill = "gksudo /bin/airmon-ng check kill"
            output_airmon_check_kill = os.popen(command_airmon_check_kill).read()
            return output_airmon_check_kill
        self.label_commands_log_output.set_text(airmonCheckKill())
        self.label_commands_log.set_text("airmon-ng check kill output:")
        grid.remove(self.button_airmon_check_kill)


    # systemd button | functionality
    def whenbutton_systemd_clicked(self, button, arg):
        if (arg=="start"):
            command_networkmanager_start= "gksudo /bin/systemctl start NetworkManager"
            output_networkmanager_start = os.popen(command_networkmanager_start).read()
            self.label_commands_log_output.set_text("NetworkManager.service has been started")
            self.label_commands_log.set_text("systemctl start NetworkManager output:")
            systemd_status=os.popen("gksudo /bin/systemctl status NetworkManager.service | awk '$1==\"Active:\" {print $0}'").read()
            self.label_systemd_status.set_text(systemd_status)
            return output_networkmanager_start
        elif (arg=="stop"):
            command_networkmanager_stop= "gksudo /bin/systemctl stop NetworkManager"
            output_networkmanager_stop= os.popen(command_networkmanager_stop).read()
            self.label_commands_log_output.set_text("NetworkManager.service has been stopped")
            self.label_commands_log.set_text("systemctl stop NetworkManager output:")
            systemd_status=os.popen("gksudo /bin/systemctl status NetworkManager.service | awk '$1==\"Active:\" {print $0}'").read()
            self.label_systemd_status.set_text(systemd_status)
            return output_networkmanager_stop


    # mainwindow button | functionality
    def Gotomainwindow(self, button):
        mainWindow = MainWindow()
        mainWindow.show_all()
        self.hide()
        
# Scan for a network
class scanWindow(Gtk.Window):

    def __init__(self, interface):

        Gtk.Window.__init__(self, title="aircrack-ng GUI | Scanning Window")
        self.connect("destroy", Gtk.main_quit)


        grid = Gtk.Grid()


        # the scrolledwindow
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        # there is always the scrollbar (otherwise: AUTOMATIC - only if needed
        # - or NEVER)
        scrolled_window.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.add(scrolled_window)
        scrolled_window.add(grid)
        self.set_default_size(800,600)
        self.set_border_width(10)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "aircrack-ng GUI | Scanning Window"
        self.set_titlebar(hb)

        label_empty_space=Gtk.Label(label="\n")
        label_empty_space_2=Gtk.Label(label="\n")
        label_empty_space_3=Gtk.Label(label="\n")

        # SSID List
        
        self.command_essid="dbus-run-session gksudo /bin/iw {} scan | egrep 'SSID:' | awk '{}'".format(interface, "{print $2}")
        output_essid= os.popen(self.command_essid).read()
#        print("\n"+output_essid+"\n")
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.listbox = Gtk.ListBox()
        items = output_essid.split()
        for item in items:
            self.listbox.add(ListBoxRowWithData(item))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()

        def filter_func(row, data, notify_destroy):
            return False if row.data == 'Fail' else True

        self.listbox.set_sort_func(sort_func, None, False)
        self.listbox.set_filter_func(filter_func, None, False)
        self.selection_listbox=None


        def on_row_activated(listbox_widget, row, grid):
            self.selection_listbox = row.data
            bssid_length = '{0,18}'
            self.ssid= self.selection_listbox
            try:
                self.bssid= os.popen("dbus-run-session gksudo /bin/iw {} scan | grep -w -B999 '{}' | grep -m 1 'BSS' | grep -E -o '^BSS.{}' | grep -oP '^BSS \K.*'".format(interface, self.selection_listbox, bssid_length)).read()
                self.channel= os.popen("dbus-run-session gksudo /bin/iw {} scan | grep -w -A999 {} | grep -m 1 -E 'DS Parameter set: channel' | grep -oP 'DS Parameter set: channel \K.*'".format(interface, self.selection_listbox)).read()
                pass
            except Exception as Thread:
                raise Thread

            self.label_ssid_output.set_text(self.ssid)
            self.label_bssid_output.set_text(self.bssid)
            self.label_channel_output.set_text(self.channel)
            return self.selection_listbox, self.ssid, self.bssid, self.channel



        # Selected AP info
        self.label_ssid=Gtk.Label(label="SSID:")
        self.label_ssid_output=Gtk.Label(label="")
        self.label_bssid=Gtk.Label(label="BSSID:")
        self.label_bssid_output=Gtk.Label(label="")
        self.label_channel=Gtk.Label(label="Channel:")
        self.label_channel_output=Gtk.Label(label="")

        self.listbox.connect('row-activated', on_row_activated, grid)
        self.box_outer.pack_start(self.listbox, True, True, 0)
        label_essid= Gtk.Label(label="SSID:")
        self.box_outer.remove(self.listbox)
        self.box_outer.add(self.listbox)

        # scanning command
        button_scan = Gtk.Button(label=f" Scan {interface}")
        button_scan.connect("clicked", self.whenbutton_scan_clicked, grid, interface)
        
        # Go back to Main Window
        self.button_mainwindow=Gtk.Button(label="Go to Main Window")
        self.button_mainwindow.connect("clicked", self.Gotomainwindow)

        # Go to Airodump-ng Window
        self.button_airodumpwindow=Gtk.Button(label="Airodump-ng")
        self.button_airodumpwindow.connect("clicked", self.Gotoairodumpwindow, interface)


        # grid
        grid.attach(self.button_mainwindow, 0, 1, 1, 1)
        grid.attach(button_scan, 0, 2, 1, 1)
        grid.attach(self.label_ssid, 0, 9, 1, 1)
        grid.attach(self.label_ssid_output, 0, 10, 1, 1)
        grid.attach(self.label_bssid, 0, 11, 1, 1)
        grid.attach(self.label_bssid_output, 0, 12, 1, 1)
        grid.attach(self.label_channel, 0, 13, 1, 1)
        grid.attach(self.label_channel_output, 0, 14, 1, 1)
        grid.attach(label_empty_space, 3, 5, 1, 1)
        grid.attach(label_empty_space_2, 0, 8, 1, 1)
        grid.attach(label_empty_space_3, 0, 16, 1, 1)
        grid.attach(self.box_outer, 0,7,1,1)
        grid.attach(self.button_airodumpwindow, 0, 16, 1, 1)

    # mainwindow button | functionality
    def Gotomainwindow(self, button):
        mainWindow = MainWindow()
        mainWindow.show_all()
        self.hide()
    
    # airodumpWindow button | functionality
    def Gotoairodumpwindow(self, button, interface):
        try:
            airodumpwindow = airodumpWindow(interface, self.ssid, self.bssid, self.channel)
            airodumpwindow.show_all()
            self.hide()
            pass
        except Exception as Thread:
            raise Thread
    
    # scan  button | functionality
    def whenbutton_scan_clicked(self, button, grid, interface):
            self.hide()
            scanwindow = scanWindow(interface)
            scanwindow.show_all()

#  Airodump-ng Window
class airodumpWindow(Gtk.Window):

    def __init__(self, interface, ssid, bssid, channel):

        Gtk.Window.__init__(self, title="aircrack-ng GUI | Airodump-ng Window")
        self.connect("destroy", Gtk.main_quit)
        grid = Gtk.Grid()

         # the scrolledwindow
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        # there is always the scrollbar (otherwise: AUTOMATIC - only if needed
        # - or NEVER)
        scrolled_window.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)

        self.add(scrolled_window)
        scrolled_window.add(grid)
        self.set_border_width(10)
        self.set_default_size(800,600)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "aircrack-ng GUI | Airodump-ng  Window"
        self.set_titlebar(hb)

        label_empty_space=Gtk.Label(label="\n")
        label_empty_space_2=Gtk.Label(label="\n")

        # Selected AP info
        self.label_ssid=Gtk.Label(label="SSID:")
        self.label_ssid_output=Gtk.Label(label=ssid)
        self.label_bssid=Gtk.Label(label="BSSID:")
        self.label_bssid_output=Gtk.Label(label=bssid)
        self.label_channel=Gtk.Label(label="Channel:")
        self.label_channel_output=Gtk.Label(label=channel)

        # airmon check & airmon check kill
        button_airmon_check = Gtk.Button(label="airmon-ng check")
        self.button_airmon_check_kill = Gtk.Button(label="airmon-ng check kill")
        self.button_airmon_check_kill.connect("clicked", self.whenbutton_airmon_check_kill_clicked, grid)
        button_airmon_check.connect("clicked", self.whenbutton_airmon_check_clicked, grid)

        #airmon start|stop {interface}
        button_airmon_start = Gtk.Button(label="airmon-ng start")
        button_airmon_start.connect("clicked", self.whenbutton_airmon_clicked, "start", interface)
        button_airmon_stop = Gtk.Button(label="airmon-ng stop")
        button_airmon_stop.connect("clicked", self.whenbutton_airmon_clicked, "stop", interface)

        # command log output
        self.label_commands_log = Gtk.Label(label='')
        self.ebox_airmon_commands_log = Gtk.EventBox()
        self.label_commands_log_output = Gtk.Label('')
        self.label_commands_log_output.set_selectable(True)
        self.label_commands_log_output.set_line_wrap_mode(True)
        self.ebox_airmon_commands_log.add(self.label_commands_log_output)


        # Systemd toggle
        self.label_systemd=Gtk.Label(label="\n In most cases, you need to stop your network manager service.\n If you are using systemd with NetworkManager.service you can stop it from here \n")
        self.button_systemd_start=Gtk.Button(label="Start NetworkManager.service")
        self.button_systemd_start.connect("clicked", self.whenbutton_systemd_clicked, "start")
        self.button_systemd_stop=Gtk.Button(label="Stop NetworkManager.service")
        self.button_systemd_stop.connect("clicked", self.whenbutton_systemd_clicked, "stop")
        label_systemd=Gtk.Label(label="\n Systemd Status: \n ")
        systemd_status=os.popen("dbus-run-session gksudo /bin/systemctl status NetworkManager.service | awk '$1==\"Active:\" {print $0}'").read()
        self.label_systemd_status=Gtk.Label(systemd_status)

        # Go back to Main Window
        self.button_mainwindow=Gtk.Button(label="Go to Main Window")
        self.button_mainwindow.connect("clicked", self.Gotomainwindow)

        self.label_current_interface=Gtk.Label(label="Current Interface:")
        self.label_current_interface_output=Gtk.Label(label="")

        # grid
        grid.attach(self.button_mainwindow, 0, 1, 1, 1)
        grid.attach(self.label_current_interface, 2, 1, 1, 1)
        grid.attach(self.label_current_interface_output, 3, 1, 1, 1)
        grid.attach(button_airmon_check, 1, 1, 1, 1)
        grid.attach(button_airmon_start, 1, 4, 1, 1)
        grid.attach(button_airmon_stop, 1, 7, 1, 1)
        grid.attach(self.label_commands_log, 1,8,1,1)
        grid.attach(self.ebox_airmon_commands_log, 1, 10, 1, 1)
        grid.attach(self.label_systemd, 1, 15, 5, 5)
        grid.attach(self.button_systemd_start, 1, 20, 1,1)
        grid.attach(self.button_systemd_stop, 1, 22, 1,1)
        grid.attach(label_systemd, 1, 23, 1,1)
        grid.attach(self.label_systemd_status, 1, 24, 1,1)
        grid.attach(self.label_ssid, 1, 27, 1, 1)
        grid.attach(self.label_ssid_output, 1, 28, 1, 1)
        grid.attach(self.label_bssid, 1, 29, 1, 1)
        grid.attach(self.label_bssid_output, 1, 30, 1, 1)
        grid.attach(self.label_channel, 1, 31, 1, 1)
        grid.attach(self.label_channel_output, 1, 32, 1, 1)


    # airmon-ng (start|stop) button | functionality
    def whenbutton_airmon_clicked(self, button, arg, interface):
        if (arg=="start"):
            command_airmon_start= f"dbus-run-session gksudo /bin/airmon-ng start {interface}"
            output_airmon_start = os.popen(command_airmon_start).read()
            self.label_commands_log_output.set_text(output_airmon_start)
            self.label_commands_log.set_text(f"dbus-run-session airmon-ng start {interface} output:")
            newInterface= os.popen("dbus-run-session gksudo airmon-ng start {} | grep 'enabled' | awk '{}' | sed -e 's/\(^.*]\)\(.*\)\().*$\)/\2/'".format(interface, "{print $9}")).read()
            print(newInterface)
            self.label_current_interface_output.set_text(newInterface)
            return output_airmon_start
        elif (arg=="stop"):
            command_airmon_stop= f"dbus-run-session gksudo /bin/airmon-ng stop {interface}"
            output_airmon_stop= os.popen(command_airmon_stop).read()
            self.label_commands_log_output.set_text(output_airmon_stop)
            self.label_commands_log.set_text(f"dbus-run-session airmon-ng stop {interface} output:")
            print(interface)
            return output_airmon_stop

    # airmon-ng check button | functionality
    def whenbutton_airmon_check_clicked(self, button, grid):
        def airmonCheck():
            command_airmon_check = "dbus-run-session gksudo /bin/airmon-ng check"
            output_airmon_check = os.popen(command_airmon_check).read()
            return output_airmon_check

        self.label_commands_log_output.set_text(airmonCheck())
        self.label_commands_log.set_text("airmon-ng check output:")
        grid.attach(self.button_airmon_check_kill,3, 12, 1, 1)
        self.show_all()
        
    # airmon-ng check kill button | functionality
    def whenbutton_airmon_check_kill_clicked(self, button, grid):
        def airmonCheckKill():
            command_airmon_check_kill = "dbus-run-session gksudo /bin/airmon-ng check kill"
            output_airmon_check_kill = os.popen(command_airmon_check_kill).read()
            return output_airmon_check_kill
        self.label_commands_log_output.set_text(airmonCheckKill())
        self.label_commands_log.set_text("airmon-ng check kill output:")
        grid.remove(self.button_airmon_check_kill)

    # systemd button | functionality
    def whenbutton_systemd_clicked(self, button, arg):
        if (arg=="start"):
            command_networkmanager_start= "dbus-run-session gksudo /bin/systemctl start NetworkManager"
            output_networkmanager_start = os.popen(command_networkmanager_start).read()
            self.label_commands_log_output.set_text("NetworkManager.service has been started")
            self.label_commands_log.set_text("systemctl start NetworkManager output:")
            systemd_status=os.popen("dbus-run-session gksudo /bin/systemctl status NetworkManager.service | awk '$1==\"Active:\" {print $0}'").read()
            self.label_systemd_status.set_text(systemd_status)
            return output_networkmanager_start
        elif (arg=="stop"):
            command_networkmanager_stop= "dbus-run-session gksudo /bin/systemctl stop NetworkManager"
            output_networkmanager_stop= os.popen(command_networkmanager_stop).read()
            self.label_commands_log_output.set_text("NetworkManager.service has been stopped")
            self.label_commands_log.set_text("systemctl stop NetworkManager output:")
            systemd_status=os.popen("dbus-run-session gksudo /bin/systemctl status NetworkManager.service | awk '$1==\"Active:\" {print $0}'").read()
            self.label_systemd_status.set_text(systemd_status)
            return output_networkmanager_stop


    # mainwindow button | functionality
    def Gotomainwindow(self, button):
        mainWindow = MainWindow()
        mainWindow.show_all()
        self.hide()



window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()



"""
        # airodump command
        button_airodump = Gtk.Button(label=f"airodump-ng {interface}")
        button_airodump.connect("clicked", self.whenbutton_airodump_clicked, grid, interface)
        self.label_airodump_output = Gtk.Label("test")
        self.textview_airodump=Gtk.TextView() 
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.textview_airodump)
        exp = Gtk.Expander()
#        exp.set_size(400,300)
#        scroll.set_default_size(400,300)
        exp.add(scroll)


        self.sub_proc = subprocess.Popen(f"/bin/ls ", stdout=subprocess.PIPE, shell=True)
        self.sub_outp = ""
        def non_block_read(output):
            fd = output.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
            try:
                self.foutput=output.read().decode("utf-8")
#                self.foutput=output.read()

                return self.foutput
                return 'hi'

            except Exception as Thread:
                raise Thread



        def update_terminal():
            self.textview_airodump.get_buffer().insert_at_cursor(non_block_read(self.sub_proc.stdout))
            return self.sub_proc.poll() is None

        gobject.timeout_add(100, update_terminal)




                cmd = ['./abc.py'] 
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
stderr=subprocess.STDOUT ) 

                while True: 
                        line = proc.stdout.readline() 
                        wx.Yield() 
                        if line.strip() == "": 
                                pass 
                        else: 
                                print line.strip() 
                                self.text_area_right.AppendText(line) # This is my update part of 
the text area 

                        if not line: 
                                break 
                proc.wait() 
                """
