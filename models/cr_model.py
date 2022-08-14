from loguru import logger


class CrModel():
    ''' posrednik mejdu controllerom i vneshnimi servisami '''

    def __init__(self, grpc_client):
        logger.info('')
        self.active_tool = None
        self.http_client = grpc_client

    async def get_cr_data(self, mach_id):
        logger.info('')
        return await self.http_client.get_measure_values_of_packet(mach_id)
