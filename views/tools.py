from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, ColorProperty
from kivy.clock import Clock
from loguru import logger


class ToolsScreen(BoxLayout):
    date_time = StringProperty('***')
    rows_layout = ObjectProperty()

    def __init__(self, **kwargs):
        logger.info('')
        super(ToolsScreen, self).__init__(**kwargs)
        self.tools_controller = App.get_running_app().tools_controller
        self.tools_controller.tools_screen = self
        Clock.schedule_once(self.init_interface, 1)  ## jdem  kogda vse ob'ekti budut sgenerirovanni

    def init_interface(self, arg=None):
        logger.info('')
        self.tools_controller.make_interface()

    def update_refreshable_interface_info(self):
        logger.info('')
        self.tools_controller.update_refreshable_interface_info()

    def show_packets_list(self):
        logger.info('')
        self.tools_controller.select_packet()


class OneRowGridLayout(GridLayout):
    bg_color = ColorProperty()
    mach_number = StringProperty()
    part_name = StringProperty()
    operator_name = StringProperty()
    data_layout = ObjectProperty()
    select_task = ObjectProperty()
    detach_task = ObjectProperty()
    open_meas_scr_button = ObjectProperty()


class OneLabelGridLayout(GridLayout):
    bg_color = ColorProperty()
    lb_text = ObjectProperty()

    def on_touch_down(self, touch, func=str):
        if touch.is_double_tap:
            func()


class FirstColGridLayout(GridLayout):
    bg_color = ColorProperty()
    first_row = StringProperty()


class SecondColGridLayout(GridLayout):
    bg_color = ColorProperty()
    first_row = StringProperty()
    second_row = StringProperty()
    third_row = StringProperty()
    fourth_row = StringProperty()


class ThirdColGridLayout(GridLayout):
    first_row = StringProperty()
    second_row = StringProperty()
    third_row = StringProperty()
    fourth_row = StringProperty()


class FourthColGridLayout(GridLayout):
    bg_color = ColorProperty()


class TasksList(GridLayout):
    tasks_layout = ObjectProperty()
    cancel_button = ObjectProperty()


class OneTask(BoxLayout):
    task_id = StringProperty()
    part_name = StringProperty()
    task_to_m_tool = ObjectProperty()


class PacketsFormLayout(BoxLayout):
    pass


class M1CausesList(GridLayout):
    materials_layout = ObjectProperty()
    cancel_button = ObjectProperty()


class SingleM1Couse(BoxLayout):
    m1_cause = StringProperty()
