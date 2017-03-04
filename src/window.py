import gtk
import gobject
import time
from threading import Thread
from dialog import DialogWindow

"""

    Threaded responsive main GUI window

"""


class WindowGUI(Thread, gtk.Window):
    active_cust_id = 0
    pause = 1

    def __init__(self, c, sql):
        Thread.__init__(self)
        self.c = c
        self.sql = sql
        self.start()

    def run(self):
        self.Window()
        gtk.gdk.threads_init()
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()

    """ Actual GUI """

    def Window(self):
        gtk.Window.__init__(self)

        self.set_title("eaglehour")

        vbox = gtk.VBox()
        self.add(vbox)

        label = gtk.Label("Client")
        vbox.pack_start(label)
        combo_box = gtk.combo_box_new_text()
        combo_box.set_wrap_width(2)
        combo_box.append_text('Interntid')
        for x in self.c.get_customers():
            combo_box.append_text(x)
        combo_box.set_active(0)

        combo_box.connect('changed', self.choose_customer)

        vbox.pack_start(combo_box)

        label = gtk.Label("Time elapsed")
        vbox.pack_start(label)
        entry = gtk.Entry()
        entry.set_text("00:00:00")
        self.current_used = 0
        self.entry = entry
        gobject.timeout_add(1000, self.update)
        vbox.pack_start(entry)

        label = gtk.Label("Total today")
        vbox.pack_start(label)
        entry = gtk.Entry()
        entry.set_text("00:00:00")
        self.total_used = 0
        self.total = entry
        vbox.pack_start(self.total)

        button = gtk.Button("Start / Stop")  # stock='gtk-media-pause')
        iconw = gtk.Image()
        iconw.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
        button.set_image(iconw)
        button.connect('clicked', self.startstop)
        vbox.pack_start(button)

        self.connect('destroy', self.hide_gtk)
        self.connect('delete_event', self.hide_gtk_wocb)

#		The appeareance of the window is not very intuitive now,
#		let the user open it from the statusicon instead :-)
#        self.show_all()

    def startstop(self, cb):
        if self.pause == 1:
            """ We are rolling.... """
            self.pause = 0
            iconw = gtk.Image()
            iconw.set_from_stock(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_MENU)
            cb.set_image(iconw)
            self.sql.startHour(self.active_cust_id)

        else:
            """ In pause mode """
            self.pause = 1
            iconw = gtk.Image()
            iconw.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
            cb.set_image(iconw)
            DialogWindow(
                self.getDescription_cb, "What did you just spend time on? Keep it simple!")
            self.sql.doneHour(self.active_cust_id, self.description)

        self.hide()

    def update(self):
        if self.pause == 0:
            self.current_used = self.current_used + 1
            self.entry.set_text(
                time.strftime("%H:%M:%S", time.gmtime(self.current_used)))
            try:
                self.total_used = self.total_used + 1
                self.total.set_text(
                    time.strftime("%H:%M:%S", time.gmtime(self.total_used)))
            except:
                1

        gobject.timeout_add(1000, self.update)

    def getDescription_cb(self, text):
        self.description = text

    def choose_customer(self, cb):
        if not self.current_used == 0:
            DialogWindow(
                self.getDescription_cb, "What did you just spend time on? Keep it simple!")
            self.sql.doneHour(self.active_cust_id, self.description)
        self.active_cust_id = cb.get_active()
        self.sql.startHour(self.active_cust_id)
        self.pause = 0
        self.entry.set_text("00:00:00")
        self.current_used = 0
        self.hide()

    def show_gtk(self, cb):
        if self.is_active():
            self.hide()
        else:
            self.set_position(gtk.WIN_POS_MOUSE)
            self.show_all()
            # self.get_focus()
            # well that didnt work, lets try a hack
            self.hide()
            self.show_all()

    def hide_gtk_wocb(self, *args):
        self.hide()
        return True

    def hide_gtk(self, cb):
        self.hide()
        return
