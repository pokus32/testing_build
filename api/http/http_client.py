import asyncio
import os
import pickle

import requests
from loguru import logger
import json

# import http
#
# import api.http.robo_srv_pb2 as robo_srv_pb2
# import api.http.robo_srv_pb2_grpc as robo_srv_pb2_grpc

MAX_MESSAGE_LENGTH = 40194304

# SERVER = '[205:448f:5785:7f4b:59ab:c9e6:dbae:2407]'
SERVER = '[202:af01:395e:4fcc:30f3:5433:f878:6e35]'
# SERVER = 'localhost'

prod_crt = os.path.join(os.path.split(__file__)[0]) + '/prod.crt'
logger.info("prod_crt", prod_crt)

class HttpClient:
    """ http client for robo server """
    api_url: str = f'https://{SERVER}:5000/api/v1'

    def __init__(self):
        logger.info('')

    async def get_tasks(self) -> list:
        logger.warning('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_tasks"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_tasks',
                                data='---', verify=prod_crt)
            result = res.json().get('data', b'')
            return pickle.loads(result)

        return await asyncio.create_task(asyncio.to_thread(req))

    async def get_tasks_fields(self, fields: list) -> list:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_tasks_fields"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_tasks_fields',
                                data=json.dumps({'fields': fields}),
                                verify=prod_crt)
            res = res.json().get('data', [])
            return res

        return await asyncio.create_task(asyncio.to_thread(req))

    async def assign_task_to_mtool(self, tool_id: str, task_id: str):
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "assign_task_to_mtool"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/assign_task_to_mtool',
                                data=json.dumps({'tool_id': tool_id, 'task_id': task_id}),
                                verify=prod_crt)
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    async def remove_task_from_mtool(self, tool_id: str) -> bool:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "remove_task_from_mtool"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/remove_task_from_mtool',
                                data=json.dumps({'tool_id': tool_id}),
                                verify=prod_crt)
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    def get_tools_ids(self) -> dict:
        logger.info('')
        params = {"method": "get_tools_ids"}
        res = requests.post(f'{self.api_url}/get_tools_ids', json=params,
                            verify=prod_crt)
        return res.json().get('data', [])

    async def get_tool_refreshable_info(self, t_id: str) -> dict:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_tools_ids"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_tool_refreshable_info',
                                data=json.dumps({'t_id': t_id}),
                                verify=prod_crt)
            return res.json()

        return await asyncio.create_task(asyncio.to_thread(req))

    async def get_ppaps_fields(self, fields: list) -> list:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_ppaps_fields"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_ppaps_fields',
                                data=json.dumps({'fields': fields}),
                                verify=prod_crt)
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    async def ins_update_task(self, task_data: dict) -> list:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "ins_update_task"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/ins_update_task',
                                data=json.dumps({'task_data': task_data}),
                                verify=prod_crt)
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    async def get_measure_values_of_packet(self, mach_id: str) -> dict:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_measure_values_of_packet"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_measure_values_of_packet',
                                data=json.dumps({'m_id': mach_id}),
                                verify=prod_crt)
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    # =================M1================
    async def get_m1_causes(self, tool_id: str) -> dict:
        logger.trace('')
        headers = {'Content-Type': 'application/json'}
        params = {"method": "get_m1_causes"}

        def req() -> requests.Response:
            res = requests.post(f'{self.api_url}/get_m1_causes',
                                data=json.dumps({'tool_id': tool_id}),
                                verify=prod_crt)
            return res.json().get('data', [])

        return await asyncio.create_task(asyncio.to_thread(req))

    # # =================StaffRequests================
    #
    # async def get_staff_requests(self) -> bytes:
    #     logger.info('')
    #     try:
    #         async with http.aio.secure_channel(
    #                 self.__server_address_port,
    #                 self.__creds,
    #                 compression=http.Compression.Gzip,
    #                 options=self.__options) as channel:
    #             aio_stub = robo_srv_pb2_grpc.roboStub(channel)
    #             arg = robo_srv_pb2.empty_request()
    #             response = await aio_stub.get_staff_requests(arg)
    #             return response.result
    #     except http.RpcError as rpc_error:
    #         logger.error(rpc_error)
    #         return b''
    #
    # async def get_last_out_n(self) -> str:
    #     logger.info('')
    #     try:
    #         async with http.aio.secure_channel(
    #                 self.__server_address_port,
    #                 self.__creds,
    #                 compression=http.Compression.Gzip,
    #                 options=self.__options) as channel:
    #             aio_stub = robo_srv_pb2_grpc.roboStub(channel)
    #             arg = robo_srv_pb2.empty_request()
    #             response = await aio_stub.get_last_out_n(arg)
    #             return response.result
    #     except http.RpcError as rpc_error:
    #         logger.error(rpc_error)
    #         return ''
    #
    # async def insert_request_data(self, data):
    #     logger.info('')
    #     try:
    #         async with http.aio.secure_channel(
    #                 self.__server_address_port,
    #                 self.__creds,
    #                 compression=http.Compression.Gzip,
    #                 options=self.__options) as channel:
    #             aio_stub = robo_srv_pb2_grpc.roboStub(channel)
    #             arg = robo_srv_pb2.insert_request_data_request()
    #             arg.data = data
    #             response = await aio_stub.insert_request_data(arg)
    #             return response.result
    #     except http.RpcError as rpc_error:
    #         logger.error(rpc_error)
    #         return None
