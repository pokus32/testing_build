from asyncio import AbstractEventLoop
from loguru import logger
from kivy.uix.popup import Popup

from models.request_model import RequestModel


class RequestController():
	""" """
	model: RequestModel
	loop: AbstractEventLoop
	
	def __init__(self, model:RequestModel, loop: AbstractEventLoop):
		logger.info('')
		self.model = model
		self.gui = None
		self.loop = loop

	async def show_ppaps_list(self, SinglePPAP, PPAPsList, aplay_ppap_data, arg=None):
		logger.info('')
		ppaps_list = PPAPsList()

		def call_back(arg):
			"""

			:param arg: 

			"""
			aplay_ppap_data(arg.ppap_id, arg.ppap_name, arg.material, arg.material_dim)
			self.ppaps_pop.dismiss()

		def make_one_row(ppap):
			"""

			:param ppap: 

			"""
			tmp_obj = SinglePPAP()
			try:
				tmp_obj.aplay_button.material = ppap['material']
				tmp_obj.aplay_button.material_dim = ppap['material_dim']
				tmp_obj.aplay_button.ppap_id = ppap['id']
				tmp_obj.aplay_button.ppap_name = ppap['part_name']
				tmp_obj.ppap_id_name = ppap['id'] + '/' + ppap['part_name']
				ppaps_list.ppaps_layout.add_widget(tmp_obj)
				tmp_obj.aplay_button.bind(on_release=call_back)
			except KeyError as e:
				logger.warning(f'{e}\non {ppap}')


		list(map(make_one_row, await self.model.get_ppaps_fields(
			['id', 'part_name', 'material', 'material_dim']
			)))

		self.ppaps_pop = Popup(title = 'Bir PPAP seç',
				content = ppaps_list,
				size_hint =(None, None),
				size =(500, 400),
				title_color = [1,0,0,1],
				title_size = 20,
				# auto_dismiss=False
				)
		ppaps_list.cancel_button.bind(on_release=self.ppaps_pop.dismiss)
		self.ppaps_pop.open()

	async def get_staff_requests(self):
		logger.info('')
		return await self.model.get_staff_requests()

	async def get_last_out_n(self):
		logger.info('')
		return await self.model.get_last_out_n()

	async def get_last_in_n(self):
		logger.info('')
		return await self.model.get_last_in_n()

	async def get_requirement_data(self, req_id):
		logger.info('')
		return await self.model.get_requirement_data(req_id)

	async def insert_request_data(self, data):
		logger.info('')
		return await self.model.insert_request_data(data)

	async def update_request_data(self, data):
		logger.info('')
		return await self.model.update_request_data(data)