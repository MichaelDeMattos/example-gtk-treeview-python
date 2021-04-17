# -*- coding: utf-8 -*-

import gi
import time
import requests
import threading
from datetime import datetime
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk
from controller import ControllerQuotation

builder = Gtk.Builder()

class Project(ControllerQuotation):
    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.init_ui(*args)

        """ Global variables """
        self.quotation = "o."
        self.title = ""
        self.lst_store = []
        self.image = ""
        self.loop = True

        """ Start create thread """
        self.create_thread()

        """ The function is given the default idle priority, glib.PRIORITY_DEFAULT_IDLE. """
        self.idle_event_id = GLib.timeout_add(300, self.update_ui)

    """ Create thread for request quotation dollar """
    def create_thread(self):
        self.thread = threading.Thread(target=self.request_api_dollar)
        self.thread.daemon = True
        self.thread.start()

    """ The function update user interface """
    def update_ui(self):
        self.lb_coin_value.set_text(" R$ " + str(round(float(self.quotation), 3)).replace(".", ","))
        self.main_window.set_title(self.title)
        self.img_status.set_from_file(self.image)
        return True

    """ Create instance for widgets content in user interface """
    def init_ui(self, *args):
        self.img_status = builder.get_object("img_status")
        self.lb_coin_value = builder.get_object("lb_coin_value")
        self.lst_quotation = builder.get_object("lst_quotation")
        self.main_window = builder.get_object("main_window")
        self.main_window.show_all()

    """ This signal destroy as main_window """
    def on_main_window_destroy(self, *args):
        """ This function delete history thas consult """
        self.delete_from_history()
        """ This function destroy thread request api dollar """
        self.loop = False
        """ The glib.source_remove() function removes the event source specified by id """
        GLib.source_remove(self.idle_event_id)
        """ This function destroy main loop Gtk """
        Gtk.main_quit()

    """ This function get key press in Gtk.Window and update Gtk.TreeView """
    def on_main_window_key_press_event(self, *args):
        key = args[1].get_keyval()[1]
        if key == Gdk.KEY_F5:  # Key F5
            self.lst_quotation.clear()
            [self.lst_quotation.append(row) for row in self.lst_store]

    """ Request quotation dollar using API """
    def request_api_dollar(self):
        """
        Response: 200 OK
        {'USD':
                {'code': 'USD',
                 'codein': 'BRL',
                 'name': 'Dólar Comercial',
                 'high': '5.6845',
                 'low': '5.5664',
                 'varBid': '0.1116',
                 'pctChange': '2',
                 'bid': '5.6829',
                 'ask': '5.6842',
                 'timestamp': '1618001998',
                 'create_date': '2021-04-09 17:59:59'}}
        """
        url = "http://economia.awesomeapi.com.br/json/all/USD-BRL"

        try:
            while self.loop == True:
                quotation = requests.get(url)
                self.lst_store = []
                if quotation.status_code == 200:
                    quotation_json = quotation.json()
                    now = datetime.now()
                    self.title = ("Consultado em "  + now.strftime("%d/%m/%y, %H:%M:%S"))
                    self.quotation = quotation_json["USD"]["bid"]

                    """ Vars content in json """
                    coin = quotation_json["USD"]["code"]
                    bid = quotation_json["USD"]["bid"]
                    ask = quotation_json["USD"]["ask"]
                    varBid = quotation_json["USD"]["varBid"]
                    date_consult = quotation_json["USD"]["create_date"]

                    """ Register history """
                    self.insert_quotation(coin, bid, ask, varBid, date_consult)

                    """ Update list store """
                    quotations = self.select_quotation()
                    [self.lst_store.append(row.values()) for row in quotations]

                    if float(quotation_json["USD"]["varBid"]) >= 0.0001:
                        self.image = "static/img/up.png"
                    else:
                        self.image = "static/img/down.png"

                    time.sleep(30)

        except Exception as error:
            print(error)


if __name__ == "__main__":
    builder.add_from_file("templates/interface.ui")
    builder.connect_signals(Project())
    Gtk.main()
