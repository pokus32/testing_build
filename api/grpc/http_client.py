import asyncio
import pickle

import requests
from loguru import logger
import json

# import grpc
#
# import api.grpc.robo_srv_pb2 as robo_srv_pb2
# import api.grpc.robo_srv_pb2_grpc as robo_srv_pb2_grpc

MAX_MESSAGE_LENGTH = 40194304

# SERVER = '[205:448f:5785:7f4b:59ab:c9e6:dbae:2407]'
SERVER = '[202:af01:395e:4fcc:30f3:5433:f878:6e35]'

class HttpClient:
    """ grpc client for robo server """
    api_url: str = f'http://{SERVER}:5000/api/v1'

    def __init__(self):
        logger.info('')
        # self.__creds = grpc.ssl_channel_credentials(cert)
        # self.__server_address_port = server_address_port
        # self.__options = [
        #     ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        #     ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        #     ('grpc.enable_http_proxy', 0)
        # ]

    # async def __post_method(self, *params: tuple, **kwargs) -> object:
    #     logger.trace('')
    #     headers = {'Content-Type': 'application/json'}
    #     async with aiohttp.ClientSession(raise_for_status=True, read_timeout=30) as session:
    #         async with session.get(self.api_url, headers=headers, params=params, **kwargs) as resp:
    #             logger.info(resp.status)
    #             if resp.status == 200:
    #                 return await resp.json()
    #             else:
    #                 logger.warning(await resp.text())
    #                 return {}  # ERROR should be returned in JSON format
    async def get_tasks(self) -> list:
        logger.warning('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_tasks"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_tasks',
                               data='---')
            result = res.json().get('data', b'')
            print(type(result))
            return pickle.loads(result)

        return await asyncio.create_task(asyncio.to_thread(req))

    # async def get_tasks(self) -> list:
    #     logger.info('')
    #     async with grpc.aio.secure_channel(
    #             self.__server_address_port,
    #             self.__creds,
    #             compression=grpc.Compression.Gzip,
    #             options=self.__options) as channel:
    #         aio_stub = robo_srv_pb2_grpc.roboStub(channel)
    #         arg = robo_srv_pb2.empty_request()
    #         res = await aio_stub.get_tasks(arg)
    #         return pickle.loads(res.tasks_data)
    async def get_tasks_fields(self, fields: list) -> list:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_tasks_fields"}
        print(fields)

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_tasks_fields',
                                data=json.dumps({'fields': fields}))
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    async def assign_task_to_mtool(self, tool_id: str, task_id: str):
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "assign_task_to_mtool"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/assign_task_to_mtool',
                                data=json.dumps({'tool_id': tool_id, 'task_id': task_id}))
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    async def remove_task_from_mtool(self, tool_id: str) -> bool:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "remove_task_from_mtool"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/remove_task_from_mtool',
                                data=json.dumps({'tool_id': tool_id}))
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    # def remove_task(self, task_id):
    #     """ Remove task from tasks list """
    #     logger.info('')
    #     with grpc.secure_channel(
    #             self.__server_address_port,
    #             self.__creds,
    #             compression=grpc.Compression.Gzip,
    #             options=self.__options
    #     ) as channel:
    #         stub = robo_srv_pb2_grpc.roboStub(channel)
    #         arg = robo_srv_pb2.remove_task_request()
    #         arg.task_id = task_id
    #         response = stub.remove_task(arg)
    #         return response.result
    def get_tools_ids(self) -> dict:
        logger.info('')
        params = {"method": "get_tools_ids"}
        res = requests.post(f'{self.api_url}/get_tools_ids', json=params)
        return res.json().get('data', [])

    #
    # def get_tool_info(self, t_id):
    #     logger.info('')
    #     with grpc.secure_channel(
    #             self.__server_address_port,
    #             self.__creds,
    #             compression=grpc.Compression.Gzip,
    #             options=self.__options
    #     ) as channel:
    #         stub = robo_srv_pb2_grpc.roboStub(channel)
    #         arg = robo_srv_pb2.mach_tool_id(id=t_id)
    #         response = stub.get_tool_info(arg)
    #         res = dict(response.tool_data)
    #         return [res, response.img_data]
    async def get_tool_refreshable_info(self, t_id: str) -> dict:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_tools_ids"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_tool_refreshable_info',
                                data=json.dumps({'t_id': t_id}))
            return res.json()

        return await asyncio.create_task(asyncio.to_thread(req))

    async def get_ppaps_fields(self, fields: list) -> list:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_ppaps_fields"}
        print(fields)

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_ppaps_fields',
                                data=json.dumps({'fields': fields}))
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    async def ins_update_task(self, task_data: dict) -> list:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "ins_update_task"}
        print(task_data)

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/ins_update_task',
                                data=json.dumps({'task_data': task_data}))
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))
    #
    # def ins_update_task(self, task_data):
    #     logger.info('')
    #     with grpc.secure_channel(
    #             self.__server_address_port,
    #             self.__creds,
    #             compression=grpc.Compression.Gzip,
    #             options=self.__options
    #     ) as channel:
    #         stub = robo_srv_pb2_grpc.roboStub(channel)
    #         arg = robo_srv_pb2.ins_update_task_request()
    #         arg.task_data = json.dumps(task_data)
    #         response = stub.ins_update_task(arg)
    #         return response.result
    async def get_measure_values_of_packet(self, mach_id: str) -> dict:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_measure_values_of_packet"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_measure_values_of_packet',
                                data=json.dumps({'m_id': mach_id}))
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

# =================M1================
    async def get_m1_causes(self, tool_id: str) -> dict:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_m1_causes"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_m1_causes',
                                data=json.dumps({'tool_id': tool_id}))
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    # # =================StaffRequests================
    #
    # async def get_staff_requests(self) -> bytes:
    #     logger.info('')
    #     try:
    #         async with grpc.aio.secure_channel(
    #                 self.__server_address_port,
    #                 self.__creds,
    #                 compression=grpc.Compression.Gzip,
    #                 options=self.__options) as channel:
    #             aio_stub = robo_srv_pb2_grpc.roboStub(channel)
    #             arg = robo_srv_pb2.empty_request()
    #             response = await aio_stub.get_staff_requests(arg)
    #             return response.result
    #     except grpc.RpcError as rpc_error:
    #         logger.error(rpc_error)
    #         return b''
    #
    # async def get_last_out_n(self) -> str:
    #     logger.info('')
    #     try:
    #         async with grpc.aio.secure_channel(
    #                 self.__server_address_port,
    #                 self.__creds,
    #                 compression=grpc.Compression.Gzip,
    #                 options=self.__options) as channel:
    #             aio_stub = robo_srv_pb2_grpc.roboStub(channel)
    #             arg = robo_srv_pb2.empty_request()
    #             response = await aio_stub.get_last_out_n(arg)
    #             return response.result
    #     except grpc.RpcError as rpc_error:
    #         logger.error(rpc_error)
    #         return ''
    #
    # async def insert_request_data(self, data):
    #     logger.info('')
    #     try:
    #         async with grpc.aio.secure_channel(
    #                 self.__server_address_port,
    #                 self.__creds,
    #                 compression=grpc.Compression.Gzip,
    #                 options=self.__options) as channel:
    #             aio_stub = robo_srv_pb2_grpc.roboStub(channel)
    #             arg = robo_srv_pb2.insert_request_data_request()
    #             arg.data = data
    #             response = await aio_stub.insert_request_data(arg)
    #             return response.result
    #     except grpc.RpcError as rpc_error:
    #         logger.error(rpc_error)
    #         return None
