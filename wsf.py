#!/usr/bin/env python 

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import os
from subprocess import *
from threading import Thread
import time
import locale
import gobject
import gen_plot
from deglist import *


encoding = locale.getpreferredencoding()
utf8conv = lambda x : unicode(x, encoding).encode('utf8')

autorun = True
cores = os.sysconf('SC_NPROCESSORS_CONF')
cores_use = cores
#import getpass
# getpass.getuser() -> user name
home = '/home/' + os.environ['USER'] + '/'
path_conf = home + '.wsfrc'

CMP, SWAN, FVCOM = range(3)
NAME, TEXTVIEW, BASE_DIR, CMP_DIR, RUN_DIR, CMP_CMD, RUN_CMD = range(7)
cmd = [(
        '', 
        'tv_cmp',
        '',
        '',
        '',
        '',
        '',
       ),
       #(
        #'WRF', 
        #'tv_wrf', 
        #home+'wrf/', 
        #home+'wrf/', 
        #home+'wrf/',
        #'',
        #'',
       #), 
       ##################################
       ### no wrf now, change INDEX
       ##################################
       (
        'SWAN', 
        'tv_swan',
        home+'swan/', 
        home+'swan/', 
        home+'swan/', 
        #'ls /',
        'make clean && make config && make mpi',
        #'ping yahoo.com -c 15',
        #'cat /home/hask/share/txt/*',
        '',
       ),
       (
        'FVCOM', 
        'tv_fvcom', 
        home+'FVCOM/', 
        home+'FVCOM/FVCOM_source/', 
        home+'FVCOM/run/',
        'make clean && make',
        'mpirun -np ' + str(cores) + ' ../FVCOM_source/fvcom chn',
       ),
      ]

n_start = [30, 55, 40]
n_end   = [31, 32, 58]
e_start = [119, 52, 32]
e_end   = [120, 36, 10]
 
class win_main(object):        
    def __init__(self):
        #self.builder = gtk.Builder()
        #self.builder.add_from_file('wsf.xml')
        #self.builder.connect_signals(
        self.glade = gtk.glade.XML('wsf.glade')
        self.win_main = self.glade.get_widget('win_main')
        self.index = 0 # map img index
        self.run = 1

        signals = {'on_win_main_destroy':gtk.main_quit,
                   'on_but_swan_clicked':(self.on_but_cmd_clicked, cmd[SWAN]),
                   'on_but_fvcom_clicked':(self.on_but_cmd_clicked, cmd[FVCOM]),
                   'on_tog_swan_clicked':(self.on_tog_cmd_clicked, cmd[SWAN]),
                   'on_tog_fvcom_clicked':(self.on_tog_cmd_clicked, cmd[FVCOM]),
                   'on_but_clear_clicked':self.on_but_clear_clicked,
                   'on_but_settings_clicked':self.on_but_settings_clicked,
                   'on_but_about_clicked':self.on_but_about_clicked,
                   'on_but_gen_plot_clicked':self.on_but_gen_plot_clicked,
                   'on_tog_animation_clicked':self.on_tog_animation_clicked,
                   'on_hscale_value_changed':self.on_hscale_value_changed,
                   'on_spn_period_value_changed':self.on_spn_period_value_changed,
                   #'on_button1_clicked':self.on_button1_clicked,
                   #'on_but_set_cancel_clicked':self.on_but_set_cancel_clicked,
                  }
        self.glade.signal_autoconnect(signals)
        #self.window = self.builder.get_object('win_main')
        self.img_map = self.glade.get_widget('img_map')
        self.img_point = self.glade.get_widget('img_point')
        self.img_map.set_from_file(cmd[FVCOM][BASE_DIR] + '.concentration/' + '1.png')
        self.hscale = self.glade.get_widget('hscale')
        self.spn_period = self.glade.get_widget('spn_period')
        self.spn_x = self.glade.get_widget('spn_x')
        self.spn_y = self.glade.get_widget('spn_y')
        self.spn_nd = self.glade.get_widget('spn_nd')
        self.spn_nm = self.glade.get_widget('spn_nm')
        self.spn_ns = self.glade.get_widget('spn_ns')
        self.spn_ed = self.glade.get_widget('spn_ed')
        self.spn_em = self.glade.get_widget('spn_em')
        self.spn_es = self.glade.get_widget('spn_es')
        self.day = 1
        self.hour = 5
        self.win_main.show_all()

    def on_spn_period_value_changed(self, widget):
        index = widget.get_value_as_int()
        self.update_img(index)
        self.hscale.set_value(index)

    def update_img(self, index):
        if self.index <> index:
            self.img_map.set_from_file(cmd[FVCOM][BASE_DIR] + 
                        '.concentration/' + str(index) + '.png')
            self.index = index

    def animation(self, widget):
        index = self.index
        while index <= 140:
            self.update_img(index)
            self.hscale.set_value(index)
            self.spn_period.set_value(index)
            time.sleep(0.1)
            index += 1
        widget.set_label('Start Animation')
        widget.set_active(False)

    def on_tog_animation_clicked(self, widget):
        if widget.get_active():
            widget.set_label('Stop Animation')
            # significant, (widget, ) not widget, 
            # otherwise animation() get gtk.Label, not gtk.ToggleButton
            t = Thread(target=self.animation, args=(widget,))
            t.start()
        else:
            pass

    def on_hscale_value_changed(self, widget):
        # hscale doesn't have get_value_as_int()
        # and it's always 11.0, set_digits(0) doesn't work
        index = int(widget.get_value())
        self.update_img(index)
        self.spn_period.set_value(index)

    # it could be def on_but_cmd_clicked(self, widget):
    def on_but_cmd_clicked(self, widget, which):
        widget.set_sensitive(False)
        self.run = 1
        t = Thread(target=self.redirect_to_textbuffer, args=(widget, which))
        t.daemon = True
        t.start()

    def redirect_to_textbuffer(self, widget, which, textview='tv_cmp', base_dir=''):
        view = self.glade.get_widget(textview)
        buffer = view.get_buffer()
        log = ''
        f_log = None
        if base_dir:
            p = Popen(which[RUN_CMD], shell=True, stdout=PIPE, stderr=STDOUT, cwd=which[RUN_DIR])
            # Sun Apr 24 19:06:25 2011 -> Apr_24_19:06:25_2011.log
            log = base_dir + time.asctime()[4:].replace(' ', '_') + '.log'
            f_log = open(log, 'w')
        else:
            p = Popen(which[CMP_CMD], shell=True, stdout=PIPE, stderr=STDOUT, cwd=which[CMP_DIR])
        while 1:
            line = p.stdout.readline()
            if not line or self.run == 0:
                break
            gtk.gdk.threads_enter()
            if f_log:
                f_log.write(line)
            iter = buffer.get_end_iter()
            buffer.place_cursor(iter)
            buffer.insert(iter, utf8conv(line))
            view.scroll_to_mark(buffer.get_insert(), 0.1)
            gtk.gdk.threads_leave()
        if base_dir:
            f_log.close()
            widget.set_label('Run ' + which[NAME])
            widget.set_active(False)
        else:
            widget.set_sensitive(True)

    def on_tog_cmd_clicked(self, widget, which):
        #if widget.get_active() and self.run:
        if widget.get_active():
            self.run = 1
            widget.set_label('Stop ' + which[NAME])
            cmd_t = Thread(target=self.redirect_to_textbuffer, args=(widget, which, which[TEXTVIEW], which[BASE_DIR]))
            cmd_t.daemon = True
            cmd_t.start()
        else:
            self.run = 0

    def on_but_clear_clicked(self, widget):
        nb_outputs = self.glade.get_widget('nb_outputs')
        index = nb_outputs.get_current_page()
        print cmd[index][TEXTVIEW]
        view = self.glade.get_widget(cmd[index][TEXTVIEW])
        buffer = view.get_buffer()
        iter_start = buffer.get_start_iter()
        iter_end = buffer.get_end_iter()
        buffer.delete(iter_start, iter_end)
        buffer.place_cursor(iter_start)

    def on_but_settings_clicked(self, widget):
        glade = gtk.glade.XML('wsf.glade')
        about = glade.get_widget('dia_settings')
        chk_autorun = glade.get_widget('chk_autorun')
        spn_core = glade.get_widget('spn_core')
        ent_swan = glade.get_widget('ent_swan')
        ent_fvcom = glade.get_widget('ent_fvcom')
        cancel = glade.get_widget('but_set_cancel')
        ok = glade.get_widget('but_set_ok')
        chk_autorun.set_active(autorun)
        spn_core.set_value(cores)
        ent_swan.set_text(cmd[SWAN][BASE_DIR])
        ent_fvcom.set_text(cmd[FVCOM][BASE_DIR])
        ok.connect('clicked', self.settings_ok, 
                   chk_autorun, spn_core, ent_swan, ent_fvcom)
        about.run()
        about.destroy()

    def on_but_about_clicked(self, widget):
        # essential, otherwise next time about will be NoneType
        self.glade = gtk.glade.XML('/home/hask/wsf/wsf.glade')
        about = self.glade.get_widget('dia_about')
        about.run()
        about.destroy()
    
    def settings_ok(self, widget, chk_autorun, spn_core, ent_swan, ent_fvcom):
        global autorun, cores_use
        autorun = chk_autorun.get_active()
        cores_use = spn_core.get_value_as_int()
        if cores_use > cores:
            glade = gtk.glade.XML('wsf.glade')
            warning = glade.get_widget('dia_msg_core')
            warning.set_markup('Your system has only ' + str(cores) + ' cores,\n'
                              'which is less than demanded.\nSet to default!')
            warning.run()
            warning.destroy()
            cores_use = cores
            # spn_core.set_value(float(cores)), seems no valuable, 
            # because the window has been destroyed

    def on_but_gen_plot_clicked(self, widget):
        x = self.spn_x.get_value_as_int()
        y = self.spn_y.get_value_as_int()
        # new input from longitude & latitude, not coordinates
        if x == self.spn_x and y == self.spn_y:
            nd = self.spn_nd.get_value_as_int()
            nm = self.spn_nm.get_value_as_int()
            ns = self.spn_ns.get_value_as_int()
            ed = self.spn_ed.get_value_as_int()
            em = self.spn_em.get_value_as_int()
            es = self.spn_es.get_value_as_int()
            # int / int = int; int / float = float
            y = int(round(deglist2sec(deglist_minus([nd, nm, ns], n_start)) / 11.0))
            x = int(round(deglist2sec(deglist_minus([ed, em, es], e_start)) / 13.0))
            if y < 0: y = 0
            if x < 0: x = 0
            self.spn_x.set_value(x)
            self.spn_y.set_value(y)
        else : # new input from coordinates
            nd, nm, ns = deglist_plus(sec2deglist(y * 11), n_start)
            self.spn_nd.set_value(nd)
            self.spn_nm.set_value(nm)
            self.spn_ns.set_value(ns)
            print nd, nm, ns
            ed, em, es = deglist_plus(sec2deglist(x * 13), e_start)
            self.spn_ed.set_value(ed)
            self.spn_em.set_value(em)
            self.spn_es.set_value(es)
            print ed, em, es

        print  x, y, '-'*20
        # time consuming, may block, so do in a thread
        t = Thread(target=self.certain_point_plot, args=(x, y))
        t.start()

    def certain_point_plot(self, x, y):
        x_t = str(x)
        y_t = str(y)
        base = cmd[FVCOM][BASE_DIR] + '.concentration/'
        dat = base + x_t + '_' + y_t + '.dat'
        png = base + x_t + '_' + y_t + '.png'
        if os.path.exists(png):
            self.img_point.set_from_file(png)
            return
        try:
            fd_w = open(dat, 'w')
        except IOError, e:
            print e

        def out_plot(i):
            fd = open(base + str(i) + '.dat', 'r')
            self.day, self.hour, datetime = gen_plot.datestr(self.day, self.hour)
            fd_w.write(datetime + ' ' + fd.readlines()[y].split()[x] + '\n')
            fd.close()
        map(out_plot, range(1, 141))
        self.day = 1
        self.hour = 5
        fd_w.close()
        gen_plot.plot(dat, png)
        self.img_point.set_from_file(png)
        

''' Drop sys_cores from config file, count it every running.
    for the sake of miss-manipulation. '''
conf_str = \
'''autorun=True
swan_dir_path='''   + cmd[SWAN][BASE_DIR]  + '''
fvcom_dir_path=''' + cmd[FVCOM][BASE_DIR] + '''
'''
 
if __name__ == '__main__':
    gobject.threads_init()
    gtk.gdk.threads_init()
    #if os.path.exists(path_conf):
        #f = open(path)
    #else:
        #f = open(path_conf, 'w')
        #f.write(conf_str)
        #sys.exit(1)
    app = win_main()
    gtk.main()

# TODO:
#   wrf
#   config file
#   self.run is global
