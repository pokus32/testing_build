# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import ColorProperty, StringProperty
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.clock import Clock

from datetime import datetime


class PartHeader(BoxLayout):

    norm_background_color = (0.90,0.89,0.82,1)


class TaskView(BoxLayout):
    red_rect = ObjectProperty()
    green_rect = ObjectProperty()
    remove_bttn = ObjectProperty()
    bttn = ObjectProperty()
    norm_background_color = ColorProperty()


    def set_mystate(self, state):
        if state == 'down':
            with self.canvas.after:
                Color(1, 0, 0, .5, mode='rgba')
                self.red_rect = Rectangle(pos=self.pos, size=self.size)
        elif self.red_rect:
            self.canvas.after.remove(self.red_rect)

    def mark_me(self, state):
        if state == 'down':
            with self.canvas.after:
                Color(0, 1, 0, .5, mode='rgba')
                self.green_rect = Rectangle(pos=self.pos, size=self.size)
        elif self.green_rect:
            self.canvas.after.remove(self.green_rect)


class HeaderTask(BoxLayout):

    norm_background_color = (0.90,0.89,0.82,1)


class TaskInputForm(BoxLayout):
    task_id             = ObjectProperty()
    drw_n               = ObjectProperty()
    part_name           = ObjectProperty()
    parts_ammaunt       = ObjectProperty()
    second_row           = ObjectProperty()
    rows_layout         = ObjectProperty()
    set_part_name_id    = ObjectProperty()
    make_parts_table    = ObjectProperty()
    set_part_name_id    = ObjectProperty()
    init                = True
    is_new              = False

    def __init__(self,**kwargs):
        super(TaskInputForm, self).__init__(**kwargs)
        self.controller = App.get_running_app().tasks_controller
        self.controller.task_input_form = self

    def assign_m_tool(self):

        self.controller.assign_m_tool()

    def remove_marked_dims(self):
        return
        self.controller.remove_marked_dims(self.part_name.text)

    def save_data(self):

        self.controller.ins_update_task()

    def set_new_task_id(self, new_task_id):

        self.controller.set_new_task_id(new_task_id)

    def set_new_task_part_name_id(self):
        if self.init:
            return
        self.controller.set_new_task_part_name_id()

    def set_new_task_quantity(self, quantity):

        self.controller.set_new_task_quantity(quantity)

    def set_new_task_finish_date(self, finish_date):

        self.controller.set_new_task_finish_date(finish_date)

    def clear_form(self):

        self.controller.clear_task_input_form()

    def insert_media(self):

        self.controller.insert_media()

    def select_ppap(self):

        self.controller.select_ppap()


class DimRow(BoxLayout):
    norm_background_color = ColorProperty()
    dim_id  = ObjectProperty()
    dim_n   = ObjectProperty()
    prefix  = ObjectProperty()
    dim     = ObjectProperty()
    postfix = ObjectProperty()
    tol_low = ObjectProperty()
    tol_up  = ObjectProperty()
    caliper = ObjectProperty()
    projector = ObjectProperty()
    cmm     = ObjectProperty()
    # mystate = ListProperty()

    rect_del = ObjectProperty()

    def __init__(self, **kwargs):
        super(DimRow, self).__init__(**kwargs)
        self.controller = App.get_running_app().controller
        self.init_state = True
        

class NewTaskInput(BoxLayout):
    tasks_layout        = ObjectProperty()
    task_input_form     = ObjectProperty()
    cur_date            = datetime.now().strftime('%d.%m.%y')
    tasks               = []

    def __init__(self,**kwargs):
        super(NewTaskInput, self).__init__(**kwargs)
        self.controller = App.get_running_app().tasks_controller
        self.controller.data_input = self
        # self.tasks = self.controller.tasks
        Clock.schedule_once(self.init_interface, 1) ## jdem  kogda vse ob'ekti budut sgenerirovanni

    def init_interface(self, arg=None):
        self.task_input_form.make_tasks_table = self.make_table
        self.make_table()

    def add_new_task(self):

        self.controller.add_new_task()

    def remove_task(self):

        self.controller.remove_task()

    def make_table(self):

        self.controller.make_tasks_table()


class SinglePPAP(BoxLayout):
    ppap_id       = StringProperty()
    ppap_id_name  = StringProperty()
    aplay_button  = ObjectProperty()


class PPAPsList(GridLayout):
    ppaps_layout    = ObjectProperty()
    cancel_button   = ObjectProperty()
