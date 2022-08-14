from loguru import logger
import pickle


class ToolModel:
	''' posrednik mejdu controllerom i vneshnimi servisami '''
	
	def __init__(self, grpc_client):
		logger.info('')
		self.tools_ids = []
		self.tasks = {}

		self.active_tool = None
		self.http_client = grpc_client
		res = self.http_client.get_tools_ids()
		self.tools_ids.extend(res)

	async def get_tool_refreshable_info(self, mach_id):
		logger.trace('')
		return await self.http_client.get_tool_refreshable_info(mach_id)

	async def get_tasks_fields(self, fields):
		logger.info('')
		return await self.http_client.get_tasks_fields(fields)

	async def assign_task_to_mtool(self, tool_id: str, task_id: str):
		logger.info('')
		return await self.http_client.assign_task_to_mtool(tool_id, task_id)

	async def remove_task_from_mtool(self, tool_id: str):
		logger.trace('')
		return await self.http_client.remove_task_from_mtool(tool_id)

	def get_data_from_m_tool(self, part_data, dim_n, tool_type):
		logger.info('')
		values = self.m_t_controller.get_measured_data(tool_type, dim_n)
		if part_data and values: ## esli poluchenny dannie ot izmeritelnogo instrumenta
			for item in part_data['dims']:
				for val in values:
					if item['dim_n'] == val:
						nok = 1
						if item['low'] <= float(values[val]) <= item['up'] or float(values[val]) == 0:
							nok = 0
						item.update({'last_m': values[val], 'nok': nok})

##======================M1========================
	
	async def get_m1_causes(self, mach_id):
		logger.info('')
		return await self.http_client.get_m1_causes(mach_id)
