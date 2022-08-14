import pickle
from loguru import logger


class RequestModel():
	""" """

	def __init__(self, grpc_client):
		logger.info('')
		self.grpc_client = grpc_client

	async def get_staff_requests(self):
		logger.info('')
		try:
			return pickle.loads(await self.grpc_client.get_staff_requests())
		except EOFError as e:
			logger.warning(e)
			return {}

	async def get_last_out_n(self):
		logger.info('')
		return await self.grpc_client.get_last_out_n()

	async def get_last_in_n(self):
		logger.info('')
		return await self.grpc_client.get_last_in_n()

	async def get_requirement_data(self, req_id):
		logger.info('')
		try:
			return pickle.loads(await self.grpc_client.get_requirement_data(req_id))
		except EOFError as e:
			logger.warning(e)
			return None

	async def insert_request_data(self, data):
		logger.info('')
		try:
			return await self.grpc_client.insert_request_data(pickle.dumps(data))
		except EOFError as e:
			logger.warning(e)
			return None

	async def get_ppaps_fields(self, fields:list) -> str:
		logger.info('')
		return await self.grpc_client.get_ppaps_fields(fields)

	async def update_request_data(self, data):
		logger.info('')
		try:
			return pickle.loads(
				await self.grpc_client.update_request_data(
					pickle.dumps(data)
					)
				)
		except EOFError as e:
			logger.warning(e)
			return None
