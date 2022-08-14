# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ColorProperty
from datetime import datetime

from loguru import logger


class ColHeader(BoxLayout):
    norm_background_color = ObjectProperty()

    def __init__(self,**kwargs):
        logger.trace('')
        super(ColHeader, self).__init__(**kwargs)
        self.norm_background_color = [0.90,0.89,0.82,1]


class DimHeader(BoxLayout):
    n_b_color = ColorProperty()

    def __init__(self,**kwargs):
        logger.trace('')
        super(DimHeader, self).__init__(**kwargs)
        self.n_b_color = [0.90,0.89,0.82,1]


class ContrRep(BoxLayout):
    label_quantity = ObjectProperty()
    i_container_n = ObjectProperty()
    label_note = ObjectProperty()
    part_id_label = ObjectProperty()
    operator_label = ObjectProperty()
    media_row = ObjectProperty()
    label_prod_date = ObjectProperty()
    machne_tool_id = ObjectProperty()
    label_control = ObjectProperty()
    header_layout = ObjectProperty()
    rows_layout = ObjectProperty()


    cur_date = datetime.now().strftime('%d.%m.%y')##sdelat obnovlenie wremeni raz v minutu
    
    def __init__(self,**kwargs):
        logger.info('')
        super(ContrRep, self).__init__(**kwargs)
        self.controller = App.get_running_app().c_r_controller
        self.app = App.get_running_app()
        self.controller.view = self


