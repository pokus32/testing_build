from loguru import logger

from api.http.http_client import HttpClient



class TaskModel():
	''' posrednik mejdu controllerom i vneshnimi servisami '''
	http_client: HttpClient
	
	def __init__(self, grpc_client: HttpClient, base64):
		logger.info('')
		self.tasks = {}
		self.tasks_new = {}

		self.active_tool = None
		self.http_client = grpc_client
		self.base64 = base64

	async def get_ppaps_fields(self, fields: list) -> list:
		logger.info('')
		return await self.http_client.get_ppaps_fields(fields)

	async def get_tasks(self) -> list:
		logger.info('')
		return await self.http_client.get_tasks()

	async def get_tasks_fields(self, fields):
		logger.info('')
		return await self.http_client.get_tasks_fields(fields)

	async def get_single_task(self, task_id):
		logger.info('')
		for task in await self.http_client.get_tasks():
			if task['id'] == task_id:
				return task

	def add_new_task(self):
		logger.info('')
		data = {'task_id': 'new_task', 'part_name_id': '***', 'quantity': 0, 'finish_date': '00-00-00', 'is_new': True}
		self.tasks.update({'new_task': data})

	def ins_update_task(self, task):
		logger.info('')
		return self.http_client.ins_update_task(task)

	def set_new_name(self, item_id, new_name):
		logger.info('')
		part = self.parts.get(item_id, None)
		if part:
			part.part_name = new_name

	def set_new_task_part_name_id(self, item_id, new_name):
		logger.info('')
		task = self.tasks.get(item_id, None)
		if task:
			task['part_name_id'] = new_name

	def set_task_new_id(self, item_id, new_id):
		logger.info('')
		task = self.tasks.get(item_id, None)
		if task:
			task['task_id'] = new_id

	def set_new_task_quantity(self, item_id, quantity):
		logger.info('')
		task = self.tasks.get(item_id, None)
		if task:
			try:
				task['quantity'] = int(quantity)
			except:
				pass

	def set_new_task_finish_date(self, item_id, date):
		logger.info('')
		task = self.tasks.get(item_id, None)
		if task:
			try:
				task['finish_date'] = date
			except:
				pass

	def remove_task(self, task_id):
		""" Remove task from tasks list """
		logger.info('')
		return self.http_client.remove_task(task_id)
