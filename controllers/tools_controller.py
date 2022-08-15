import asyncio
from datetime import datetime

from kivy.core.window import Window
from kivy.uix.popup import Popup
from loguru import logger
from views.tools import TasksList, OneRowGridLayout

alarm_bg_colors = {'red': (3, 0, 0, 1), 'yellow': (3, 2.49, 0, 1), 'green': (0, 3, 0, 1),
                   'no_alarm': (0.9, 0.9, 0.9, 1)}
m1_bg_colors = {'True': [2, 1, 0, 1], 'False': [0, 0.75, 0, 1]}


class ToolsController():
    """ posrednik mejdu view i servisami """
    tasks_pop: Popup

    def __init__(self, app, popup: Popup, model,
                 one_task, packets_form_layout,
                 m1_causesList, singleM1Couse, cr_controller):
        logger.info('')
        self.app = app
        self.popup = popup
        self.model = model
        self.tasks = model.tasks
        self.packets_form_layout = packets_form_layout
        self.cr_controller = cr_controller

        self.one_task = one_task
        self.tools_screen = None
        self.rows_dict = {}
        self.m1_causesList = m1_causesList
        self.singleM1Couse = singleM1Couse

    async def update_refreshable_interface_info(self, arg=None):
        logger.trace('')
        # TODO: Move assigning date_time to independent async function, for smooth periodic update.
        self.tools_screen.date_time = datetime.now().strftime("%d:%m:%y") + "\n" + datetime.now().strftime("%H:%M:%S")
        for m_id in self.model.tools_ids:
            item = await self.model.get_tool_refreshable_info(m_id)
            item = item.get('data', {})

            tool_id = item.get('mach_id', '---')
            mach_tool_part_count = item.get('mach_tool_part_count', '---')
            # task_part_count is not used any ware
            task_parts_count = item.get('task_part_count', '---')
            task_id = item.get('task_id', '---')
            part_name = item.get('part_name', '---')
            material = item.get('material_id', '---')
            drw_number = item.get('drw_id', '---')

            cycle_period = item.get('cycle_period', '---')
            last_measurement_date_time = item.get('last_measurement_date_time', '---')
            packet_id = item.get('packet_id', '---')
            operator = item.get('operator_id', '---')

            self.rows_dict[m_id].tool_id = tool_id
            self.rows_dict[m_id].m1_button.background_color = m1_bg_colors[str(bool(item.get('m1', [])))]
            self.rows_dict[m_id].alarm_button.background_color = alarm_bg_colors[item.get('alarm', 'no_alarm')]
            self.rows_dict[m_id].last_control_date = ' Son ölçü: ' + last_measurement_date_time
            self.rows_dict[m_id].packet_id = str(packet_id)
            self.rows_dict[m_id].part_count = str(mach_tool_part_count)

            self.rows_dict[m_id].cycle_time = str(cycle_period)
            self.rows_dict[m_id].operator_name = str(operator)
            self.rows_dict[m_id].task_id = str(task_id)
            self.rows_dict[m_id].part_name = str(part_name)
            self.rows_dict[m_id].material = str(material)
            self.rows_dict[m_id].drw_number = str(drw_number)
            self.rows_dict[m_id].task_parts_count = str(task_parts_count)
            self.rows_dict[m_id].open_cr_scr.part_name = str(part_name)
            self.rows_dict[m_id].open_cr_scr.tool_id = tool_id
            self.rows_dict[m_id].open_cr_scr.operator = str(operator)
        await asyncio.sleep(3)  # waiting 1 second before execute self.schedule_update_refreshable_interface_info()
        self.schedule_update_refreshable_interface_info()

    def make_interface(self):
        logger.info('')
        i = 1
        self.tools_screen.rows_layout.clear_widgets()
        if not self.model.tools_ids:
            return
        for m_id in self.model.tools_ids:
            if i % 2:
                bg_color = [0.70, 0.89, 0.82, 1]
            else:
                bg_color = [0.81, 0.89, 0.82, 1]
            tmp_obj = OneRowGridLayout()
            tmp_obj.bg_color = bg_color
            tmp_obj.m1_button.bind(on_release=self.show_m1_causes)
            tmp_obj.select_task.bind(on_release=self.select_task)
            tmp_obj.detach_task.bind(on_release=self.remove_task_from_mtool)
            tmp_obj.open_cr_scr.bind(on_release=self.open_cr_scr)
            self.tools_screen.rows_layout.add_widget(tmp_obj)
            self.rows_dict.update({m_id: tmp_obj})
            i += 1
        self.schedule_update_refreshable_interface_info()

    def schedule_update_refreshable_interface_info(self):
        logger.trace('')
        loop = asyncio.get_event_loop()
        tool_info_coro = loop.create_task(self.update_refreshable_interface_info())
        asyncio.gather(tool_info_coro, return_exceptions=False)

    def show_m1_causes(self, arg):
        logger.info('')
        async def show_m1_causes(tool_id):
            m1_causes_list = await self.model.get_m1_causes(tool_id)
            if m1_causes_list[0] == '':  # TODO make reliable verification
                return
            m1_causes_list_widget = self.m1_causesList()
            for cause in m1_causes_list:
                tmp_obj = self.singleM1Couse()
                tmp_obj.m1_cause = cause
                m1_causes_list_widget.main_layout.add_widget(tmp_obj)

            m1_causes = self.popup(title='M1 Sebebleri:',
                                   content=m1_causes_list_widget,
                                   size_hint=(None, None),
                                   size=("300sp", "400sp"),
                                   title_color=[1, 0, 0, 1],
                                   title_size="20sp",
                                   # auto_dismiss=False
                                   )
            m1_causes_list_widget.cancel_button.bind(on_release=m1_causes.dismiss)
            m1_causes.open()

        asyncio.gather(asyncio.ensure_future(
            show_m1_causes(arg.tool_id)
        ), return_exceptions=False)

    def open_cr_scr(self, arg):
        logger.info('')
        self.app.rt_wdt.open_tab(2)
        asyncio.gather(asyncio.ensure_future(
            self.cr_controller.fill_view(arg.part_name, arg.tool_id, arg.operator)
        ), return_exceptions=False)

    def select_task(self, arg):
        logger.info('')
        tasks_list = TasksList()
        tasks_list.tasks_layout.clear_widgets()

        async def show_popup():
            print('Window.size', Window.size)
            for task in await self.model.get_tasks_fields(['id', 'ppap.part.part_name']):
                if not task:
                    continue
                tmp_obj = self.one_task()
                tmp_obj.task_id = task['task_id']
                tmp_obj.tool_id = arg.tool_id
                tmp_obj.part_name = task['part_name']
                tmp_obj.task_to_m_tool.bind(on_release=self.assign_task_to_mtool)
                tasks_list.tasks_layout.add_widget(tmp_obj)

            self.tasks_pop = self.popup(title=f'MakNo{arg.tool_id} için, bir emir seç.',
                                        content=tasks_list,
                                        size_hint=(None, None),
                                        size=("450sp", "500sp"),
                                        title_color=[1, 0, 0, 1],
                                        title_size="20sp",
                                        # auto_dismiss=False
                                        )
            tasks_list.cancel_button.bind(on_release=self.tasks_pop.dismiss)
            self.tasks_pop.open()

        asyncio.gather(asyncio.ensure_future(
            show_popup()
        ), return_exceptions=False)

    def remove_task_from_mtool(self, instance):
        asyncio.gather(asyncio.ensure_future(
            self.model.remove_task_from_mtool(instance.tool_id)
        ), return_exceptions=False)

    def assign_task_to_mtool(self, arg):
        logger.info('')

        async def task_to_mtool():
            if await self.model.assign_task_to_mtool(arg.parent.tool_id, arg.parent.task_id):
                self.tasks_pop.dismiss()

        asyncio.gather(asyncio.ensure_future(
            task_to_mtool()
        ), return_exceptions=False)
