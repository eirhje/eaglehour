import gtk

#
# Creates a dialog for user input. Triggers on pressing OK or ENTER.
#
# Usage:
#
#	def callback(text):
#	        print text
#	DialogWindow(callback, "Description of what you've worked with. Keep it short, simple and stupid!")
#
class DialogWindow(gtk.Window):
	def __init__(self, callback, text):
		dialog = gtk.Dialog("User Input Required", self, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK))
	
		self.dialog = dialog
		self.callback = callback

		label = gtk.Label(text)
		dialog.vbox.pack_start(label)

		self.entry = gtk.Entry()
		self.entry.connect("activate", self.got_enter_or_ok)
		dialog.vbox.pack_start(self.entry)

		dialog.show_all()
		response = dialog.run()
		self.callback(self.entry.get_text())

	# To destroy the window when the hitting ENTER, for usability
	def got_enter_or_ok(self, *args):
		self.dialog.destroy()
