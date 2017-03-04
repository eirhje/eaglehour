import gtk
from threading import Thread

"""

    Threaded responsive GTK system icon :-)

"""


class StatusIcon(Thread):

    def __init__(self, wg):
        Thread.__init__(self)
        self.wg = wg
        self.start()

    def run(self):
        self.statusIcon()
        gtk.gdk.threads_init()
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()

    def make_menu(self, event_button, event_time, icon):
        menu = gtk.Menu()
        item = gtk.MenuItem("Quit")
        item.connect('activate', self.do_quit)
        item.show()
        menu.append(item)
        menu.popup(None, None,
                   gtk.status_icon_position_menu, event_button, event_time, icon)

    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time, icon)

    def statusIcon(self, parent=None):
        icon = gtk.status_icon_new_from_stock(gtk.STOCK_INDEX)
        icon.connect('popup-menu', self.on_right_click)
        icon.connect('activate', self.wg.show_gtk)

    def do_quit(self, callback):
        exit(0)

    def pos(self):
        return self.get_position()
