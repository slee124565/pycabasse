# 安裝必要套件
# pip install async-upnp-client  # 這一行通常只需要執行一次

# 發現設備範例
import asyncio
from async_upnp_client.client_factory import UpnpFactory, UpnpDevice
from async_upnp_client.aiohttp import AiohttpRequester


async def discover_devices():
    requester = AiohttpRequester()
    factory = UpnpFactory(requester)
    devices = await factory.discover(timeout=5)  # 增加 timeout 避免無限等待
    for device in devices:
        if "Cabasse" in device.friendly_name:
            print(f"Found Cabasse device: {device.location}")
    factory.shutdown()  # 釋放資源


asyncio.run(discover_devices())
