import asyncio

from kivy.core.window import Window
from loguru import logger
import os
import base64

import kivy

from kivy.app import App
from kivy.uix.popup import Popup
# from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.cache import Cache

from api.grpc.http_client import HttpClient
from controllers.tasks_controller import TasksController
from controllers.tools_controller import ToolsController
from controllers.c_rep_controller import CRController
from controllers.request_controller import RequestController
from models.cr_model import CrModel
from models.task_model import TaskModel
from models.tool_model import ToolModel
from models.request_model import RequestModel
from views.tasks_list import SinglePPAP, TaskView, PPAPsList
from views.tools import OneTask, PacketsFormLayout
from views.tools import M1CausesList, SingleM1Couse
from views.contr_rep import DimHeader, ColHeader
from views.req_layout import ReqLayout

server_address_port = '192.168.1.42:50051'

#kivy.require('2.0.0')

Cache.register('media', limit=100, timeout=60 * 60 * 10)

fileDir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(fileDir, 'views', 'qc.kv')
Builder.load_file(filename)
filename = os.path.join(fileDir, 'views', 'tasks_list.kv')
Builder.load_file(filename)
filename = os.path.join(fileDir, 'views', 'tools.kv')
Builder.load_file(filename)
filename = os.path.join(fileDir, 'views', 'contr_rep.kv')
Builder.load_file(filename)
filename = os.path.join(fileDir, 'views', 'req_layout.kv')
Builder.load_file(filename)


class RootWidget(BoxLayout):
    tools_screen = ObjectProperty()
    tabbed_panel = ObjectProperty()

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def open_tab(self, tab_id=1):
        self.tabbed_panel.switch_to(self.tabbed_panel.tab_list[tab_id])


class QCApp(App):

    def __init__(self, loop: asyncio.AbstractEventLoop, **kwargs):
        super(QCApp, self).__init__(**kwargs)

        self.grpc_client = HttpClient()
        self.cr_model = CrModel(self.grpc_client)
        self.taskModel = TaskModel(self.grpc_client, base64)
        self.toolModel = ToolModel(self.grpc_client)
        self.tasks_controller = TasksController(self.taskModel, TaskView, SinglePPAP, PPAPsList)
        self.c_r_controller = CRController(self.cr_model, DimHeader, ColHeader)
        self.tools_controller = ToolsController(App.get_running_app(), Popup, self.toolModel,
                                                OneTask, PacketsFormLayout,
                                                M1CausesList, SingleM1Couse, self.c_r_controller)
        self.request_model = RequestModel(self.grpc_client)
        self.request_controller = RequestController(self.request_model, loop)
        self.rt_wdt = RootWidget()

    def build(self):
        logger.info('QCApp.build')
        self.title = 'ÜRETİM SORUMLUSU'
        # Window.size = (720, 1280)

        return self.rt_wdt


if __name__ == '__main__':
    logger.info('Starting app. QCApp().run()')
    loop = asyncio.get_event_loop()
    app_coro = QCApp(loop).async_run(async_lib='asyncio')
    asyncio.run(app_coro)
    loop.close()
