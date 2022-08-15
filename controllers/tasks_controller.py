from kivy.uix.popup import Popup
from kivy.uix.button import Button
from loguru import logger
import asyncio

from models.task_model import TaskModel


class TasksController():
    ''' posrednik mejdu view i servisami '''
    model: TaskModel
    ppaps_pop: Popup

    def __init__(self, model: TaskModel, taskView, singlePPAP, PPAPsList):
        logger.info('')
        self.taskView = taskView
        self.singlePPAP = singlePPAP
        self.ppapsList = PPAPsList
        self.model = model
        self.task_input_form = None
        self.data_input = None
        self.selected_task = {"id": "", "quantity": 0, "finish_date": "", "ppap_id": "", "state": {"quantity": 0}}

    def ins_update_task(self):
        logger.info('')

        async def ins_update_t():
            if all(self.selected_task.values()):
                if await self.model.ins_update_task(self.selected_task):
                    self.clear_task_input_form()
                    self.make_tasks_table()

        asyncio.gather(asyncio.ensure_future(
            ins_update_t()
        ), return_exceptions=False)

    def set_new_task_id(self, new_task_id):
        logger.info('')
        self.selected_task.update({'id': new_task_id})

    # item_id = self.task_input_form.task_id.item_id
    # new_id = self.task_input_form.task_id.text
    # self.model.set_task_new_id(item_id, new_id)

    def set_new_task_part_name_id(self):
        logger.info('')
        if self.task_input_form.task_id.text and self.task_input_form.part_name_id.text:
            self.model.set_new_task_part_name_id(self.task_input_form.task_id.item_id,
                                                 self.task_input_form.part_name_id.text)

    def set_new_task_quantity(self, quantity):
        logger.info('')
        self.selected_task.update({'quantity': quantity})

    # if self.task_input_form.task_id.text and self.task_input_form.quantity.text:
    # 	self.model.set_new_task_quantity(self.task_input_form.task_id.item_id, self.task_input_form.quantity.text)

    def set_new_task_finish_date(self, finish_date):
        logger.info('')
        self.selected_task.update({'finish_date': finish_date})

    # if self.task_input_form.task_id.text and self.task_input_form.finish_date.text:
    # 	self.model.set_new_task_finish_date(self.task_input_form.task_id.item_id, self.task_input_form.finish_date.text)

    def fill_task_input_form(self, button: Button):
        logger.info('')

        def done_callback(arg: asyncio.Future):
            logger.info('')
            self.clear_task_input_form()
            task = arg.result()[0]

            self.task_input_form.task_id.item_id = button.item_id  ## id of a task
            self.task_input_form.task_id.text = task.get('id', '---')
            self.task_input_form.ppap_id.text = task.get('ppap_id', '---')
            self.task_input_form.quantity.text = str(task.get('quantity', '0'))
            self.task_input_form.finish_date.text = task.get('finish_date', '---')

        if button.state == 'down':
            coro = asyncio.ensure_future(
                self.model.get_single_task(button.item_id)
            )
            task = asyncio.gather(coro, return_exceptions=False)
            task.add_done_callback(done_callback)
        else:
            self.clear_task_input_form()

    def clear_task_input_form(self):
        logger.info('')
        self.task_input_form.task_id.text = ''
        self.task_input_form.ppap_id.text = ''
        self.task_input_form.quantity.text = ''
        self.task_input_form.finish_date.text = ''
        self.task_input_form.rows_layout.clear_widgets()

    # def show_image(self, arg):
    # 	logger.info('')
    # 	show_image(arg.filename)

    ## ==============================DATA INPUT===========================

    def add_new_task(self):
        logger.info('')
        self.model.add_new_task()
        self.clear_task_input_form()
        self.make_tasks_table()

    def make_tasks_table(self):
        logger.info('')

        def done_callback(arg: asyncio.Future):
            logger.info('')
            self.data_input.tasks_layout.clear_widgets()
            i = 1
            for task in arg.result()[0]:
                if i % 2:
                    bg_color = [0.70, 0.89, 0.82, 1]
                else:
                    bg_color = [0.81, 0.89, 0.82, 1]
                if task:
                    tmp_obj = self.taskView()
                    tmp_obj.norm_background_color = bg_color
                    tmp_obj.task_id = task.get('id', '---')  # ne izmenyaemoe imya
                    tmp_obj.ppap_id = task.get('ppap_id', '---')
                    tmp_obj.quantity = str(task.get('quantity', '0'))
                    tmp_obj.finish_date = task.get('finish_date', '---')
                    tmp_obj.bttn.bind(on_release=self.fill_task_input_form)
                    self.data_input.tasks_layout.add_widget(tmp_obj)
                i += 1

        coro = asyncio.ensure_future(
            self.model.get_tasks_fields(['id', 'ppap_id', 'quantity', 'finish_date'])
        )
        task = asyncio.gather(coro, return_exceptions=False)
        task.add_done_callback(done_callback)

    def remove_task(self):
        logger.info('')
        for item in self.data_input.tasks_layout.children:
            if item.remove_bttn.state == 'down':
                self.model.remove_task(item.remove_bttn.item_id)
        self.clear_task_input_form()
        self.make_tasks_table()

    def select_ppap(self):
        logger.info('')
        task: asyncio.Future

        def done_callback(arg: asyncio.Future):
            ppaps_list = self.ppapsList()
            for ppap in arg.result()[0]:
                tmp_obj = self.singlePPAP()
                tmp_obj.ppap_id = ppap['id']
                tmp_obj.ppap_id_name = ppap['id'] + '/' + ppap['part_name']
                ppaps_list.ppaps_layout.add_widget(tmp_obj)
                tmp_obj.aplay_button.bind(on_release=self.assign_ppap)

            self.ppaps_pop = Popup(title='Bir PPAP seç',
                                   content=ppaps_list,
                                   size_hint=(None, None),
                                   size=("500sp", "400sp"),
                                   title_color=[1, 0, 0, 1],
                                   title_size="20sp",
                                   # auto_dismiss=False
                                   )
            ppaps_list.cancel_button.bind(on_release=self.ppaps_pop.dismiss)
            self.ppaps_pop.open()

        coro = asyncio.ensure_future(
            self.model.get_ppaps_fields(['id', 'part_name'])
        )
        task = asyncio.gather(coro, return_exceptions=False)
        task.add_done_callback(done_callback)

    def assign_ppap(self, arg=None):
        logger.info('')
        if arg:
            self.task_input_form.ppap_id.text = arg.parent.ppap_id_name
            self.selected_task.update({'ppap_id': arg.parent.ppap_id})
            self.ppaps_pop.dismiss()
