#!/usr/bin/env python 

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
 
class win_main(object):        
    def __init__(self):
        #self.builder = gtk.Builder()
        #self.builder.add_from_file("hybrid2.xml")
        self.glade = gtk.glade.XML("hybrid2.glade")
        self.win_main = self.glade.get_widget("win_main")
        #self.builder.connect_signals(
        events = {"on_win_main_destroy":gtk.main_quit,
             #"on_toggle_swan_toggled" : self.toggle_swan_toggled,
             #"on_toggle_fvcom_toggled" : self.toggle_fvcom_toggled,
             "on_but_settings_clicked":self.on_but_settings_clicked}
        self.glade.signal_autoconnect(events)
        #self.window = self.builder.get_object("win_main")
        self.win_main.show()

    #def on_toggle_swan_toggled(self):
    def on_but_settings_clicked(self, widget_type):
        #print "hinaoo"
        #self.textview = self.glade.get_widget("textview")
        #self.textview.set_text("nihaoo")

        about = gtk.AboutDialog()
        about.set_program_name("Hybrid")
        about.set_version("0.1")
        #about.set_copyright("(c) Yang Zhang")
        about.set_comments("Hybrid is a composition of SWAN/FVCOM")
        #about.set_website("")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("hybrid.png"))
        about.run()
        about.destroy()


#class win_settintgs(object):
    #def __init__(self):
        #pass

    #def run(self):
        #self.glade = gtk.glade.XML("fvcom.glade", "win_settintgs")
        #win_settintgs = self.glade.get_widget("win_settintgs")
        #win_settintgs.run()
        
 
if __name__ == "__main__":
    app = win_main()
    gtk.main()
