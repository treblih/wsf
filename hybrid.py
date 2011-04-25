#!/usr/bin/env python 

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import glib
import os
from subprocess import *
import time

#import getpass
# getpass.getuser() -> user name
autorun = True
cores = os.sysconf('SC_NPROCESSORS_CONF')
cores_use = cores
home = '/home/' + os.environ['USER'] + '/'
path_conf = home + '.hybridrc'
NAME, BASE_DIR, CMP_DIR, RUN_DIR, CMP, RUN = range(6)
cmd = {'wrf':  ('wrf', 
                home+'wrf/', 
                home+'wrf/', 
                home+'wrf/',
                '',
                ''
               ), 
       'swan': ('swan', 
                home+'swan/', 
                home+'swan/', 
                home+'swan/', 
                'make clean && make config && make mpi',
                ''
               ),
       'fvcom':('fvcom', 
                home+'FVCOM/', 
                home+'FVCOM/FVCOM_source/', 
                home+'FVCOM/run/',
                'make clean && make',
                'mpirun -np ' + str(cores) + '../FVCOM_source/fvcom chn'
               )
      }
 
class win_main(object):        
    def __init__(self):
        #self.builder = gtk.Builder()
        #self.builder.add_from_file('hybrid2.xml')
        #self.builder.connect_signals(
        self.glade = gtk.glade.XML('hybrid2.glade')
        self.win_main = self.glade.get_widget('win_main')
        self.textview = self.glade.get_widget('textview')
        self.textbuffer = self.textview.get_buffer()
        #self.textbuffer.set_text("nihao\nwakkak\n")
        signals = {'on_win_main_destroy':gtk.main_quit,
                   'on_but_swan_clicked':(self.on_but_cmd_clicked, cmd['swan']),
                   'on_but_fvcom_clicked':(self.on_but_cmd_clicked, cmd['fvcom']),
                   'on_toggle_swan_clicked':(self.on_toggle_cmd_clicked, cmd['swan']),
                   'on_toggle_fvcom_clicked':(self.on_toggle_cmd_clicked, cmd['fvcom']),
                   'on_but_settings_clicked':self.on_but_settings_clicked,
                   'on_but_about_clicked':self.on_but_about_clicked,
                   #'on_but_set_cancel_clicked':self.on_but_set_cancel_clicked,
                  }
        self.glade.signal_autoconnect(signals)
        #self.window = self.builder.get_object('win_main')
        self.win_main.show_all()

    def on_but_cmd_clicked(self, widget, which):
        widget.set_sensitive(False)
        #os.chdir(which[CMP_DIR])
        proc = Popen(which[CMP], shell=True, stdout=PIPE, stderr=STDOUT)
        glib.io_add_watch(proc.stdout, glib.IO_IN, self.write_to_buffer, 
                          '', self.textbuffer, widget)

    def on_toggle_cmd_clicked(self, widget, which):
        widget.set_active(False)
        os.chdir(which[RUN_DIR])
        proc = Popen(which[RUN],shell=True, stdout=PIPE, stderr=STDOUT)
        # Sun Apr 24 19:06:25 2011 -> Apr_24_19:06:25_2011.log
        f_log = open(which[BASE_DIR] + time.asctime()[4:].replace(' ', '_') + '.log', 'w')
        glib.io_add_watch(proc.stdout, glib.IO_IN, self.write_to_buffer,
                          f_log, self.textbuffer, widget)
        #while True:
            #line = proc.stdout.readline()
            #if not line:
                #break
            #self.textbuffer.insert_at_cursor(line)

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
        ent_swan.set_text(cmd['swan'][PATH])
        ent_fvcom.set_text(cmd['fvcom'][PATH])
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

    def write_to_buffer(self, fd, condition, f_log, textbuffer, widget):
        #if condition == glib.IO_IN: #IF THERE'S SOMETHING INTERESTING TO READ
        line = fd.readline()
        if line:
            textbuffer.insert_at_cursor(line) # WHEN RUNNING DON'T TOUCH THE TEXTVIEW!!
            if f_log:
                f_log.write(line)
            return True # FUNDAMENTAL, OTHERWISE THE CALLBACK ISN'T RECALLED
        else:
            # gtk.Button
            print 'HEHEHEHHE----------'
            if hasattr(widget, 'set_sensitive'):
                print 'sensitive'
                widget.set_sensitive(True)
            # gtk.ToggleButton
            else: 
                print 'active'
                widget.set_active(True)
            return False
    
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
        

''' Drop sys_cores from config file, count it every running.
    for the sake of miss-manipulation. '''
conf_str = \
'''autorun=True
swan_dir_path='''   + cmd['swan'][BASE_DIR]  + '''
fvcom_dir_pathm=''' + cmd['fvcom'][BASE_DIR] + '''
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
