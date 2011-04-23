#!/usr/bin/env python 

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import os, sys

#import getpass
# getpass.getuser() -> user name
autorun = True
cores = os.sysconf('SC_NPROCESSORS_CONF')
cores_use = cores
home = '/home/' + os.environ['USER'] + '/'
path_conf = home + '.hybridrc'
path_swan = home + 'swan'
path_fvcom = home + 'fvcom'
 
class win_main(object):        
    def __init__(self):
        #self.builder = gtk.Builder()
        #self.builder.add_from_file('hybrid2.xml')
        #self.builder.connect_signals(
        self.glade = gtk.glade.XML('hybrid2.glade')
        self.win_main = self.glade.get_widget('win_main')
        self.textview = self.glade.get_widget('textview')
        #self.textview.set_buffer('nihao\nwakak\n')
        events = {'on_win_main_destroy':gtk.main_quit,
                 #'on_toggle_swan_toggled' : self.toggle_swan_toggled,
                 #'on_toggle_fvcom_toggled' : self.toggle_fvcom_toggled,
                  'on_but_settings_clicked':self.on_but_settings_clicked,
                  'on_but_about_clicked':self.on_but_about_clicked,
                  #'on_but_set_cancel_clicked':self.on_but_set_cancel_clicked,
                 }
        self.glade.signal_autoconnect(events)
        #self.window = self.builder.get_object('win_main')
        self.win_main.show()

    #def on_toggle_swan_toggled(self):
        #print 'hinaoo'

    def on_but_settings_clicked(self, widget):
        glade = gtk.glade.XML('hybrid2.glade')
        about = glade.get_widget('dia_settings')
        chk_autorun = glade.get_widget('chk_autorun')
        spn_core = glade.get_widget('spn_core')
        ent_swan = glade.get_widget('ent_swan')
        ent_fvcom = glade.get_widget('ent_fvcom')
        cancel = glade.get_widget('but_set_cancel')
        ok = glade.get_widget('but_set_ok')
        chk_autorun.set_active(autorun)
        spn_core.set_value(cores)
        ent_swan.set_text(path_swan)
        ent_fvcom.set_text(path_fvcom)
        ok.connect('clicked', self.settings_ok, 
                   chk_autorun, spn_core, ent_swan, ent_fvcom)
        about.run()
        about.destroy()

    def on_but_about_clicked(self, widget):
        # essential, otherwise next time about will be NoneType
        glade = gtk.glade.XML('hybrid2.glade')
        about = glade.get_widget('dia_about')
        about.run()
        about.destroy()
        #about = gtk.AboutDialog()
        #about.set_program_name('Hybrid')
        #about.set_version('0.1')
        #about.set_copyright('(c) Yang Zhang')
        #about.set_comments('Hybrid is a composition of SWAN/FVCOM')
        #about.set_website('http://github.com/treblih/hybrid.git')
        #about.set_logo(gtk.gdk.pixbuf_new_from_file('hybrid.png'))
        #about.run()
        #about.destroy()
    
    def settings_ok(self, widget, chk_autorun, spn_core, ent_swan, ent_fvcom):
        global autorun, cores_use
        autorun = chk_autorun.get_active()
        cores_use = spn_core.get_value_as_int()
        if cores_use > cores:
            glade = gtk.glade.XML('hybrid2.glade')
            warning = glade.get_widget('dia_msg_core')
            warning.set_markup('Your system has only ' + str(cores) + ' cores,\n'
                              'which is less than demanded.\nSet to default!')
            warning.run()
            warning.destroy()
            cores_use = cores
        


#class win_settintgs(object):
    #def __init__(self):
        #pass

    #def run(self):
        #self.glade = gtk.glade.XML('fvcom.glade', 'win_settintgs')
        #win_settintgs = self.glade.get_widget('win_settintgs')
        #win_settintgs.run()

''' Drop sys_cores from config file, count it every running.
    for the sake of miss-manipulation. '''
conf_str = \
'''autorun=True
path_swan=''' +  path_swan + '''
path_fvcom=''' + path_fvcom + '''
'''
 
if __name__ == '__main__':
    #if os.path.exists(path_conf):
        #f = open(path)
    #else:
        #f = open(path_conf, 'w')
        #f.write(conf_str)
        #sys.exit(1)
    app = win_main()
    gtk.main()
