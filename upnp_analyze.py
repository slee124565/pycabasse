import asyncio
import argparse
from async_upnp_client.client_factory import UpnpFactory
from async_upnp_client.ssdp_listener import SsdpListener


async def discover_and_analyze_upnp(target_ip):
    ssdp = SsdpListener()
    try:
        await ssdp.async_start()

        # 使用參數化IP進行裝置探索
        devices = await ssdp.async_search(target_ip=target_ip)

        # 過濾目標裝置
        target_device = next(
            (d for d in devices if d.location.host == target_ip),
            None
        )

        if not target_device:
            raise ValueError(f"未找到IP為 {target_ip} 的UPnP裝置")

        # 建立裝置實例
        factory = UpnpFactory()
        device = await factory.async_create_device(target_device.location)

        # 輸出裝置資訊
        print(f"裝置基本資訊 [IP: {target_ip}]:")
        print(f"名稱: {device.name}\n廠商: {device.manufacturer}\n型號: {device.model_name}\n")

        # 列舉服務清單
        print("支援的UPnP服務:")
        for service in device.services.values():
            print(f"• 服務類型: {service.service_type}")
            print(f"  控制URL: {service.control_url}")
            print(f"  可用動作: {[a.name for a in service.actions.values()]}\n")

    except Exception as e:
        print(f"發生錯誤: {str(e)}")
    finally:
        await ssdp.async_stop()


if __name__ == "__main__":
    # 設定命令列參數解析器
    parser = argparse.ArgumentParser(description='UPnP裝置分析工具')
    parser.add_argument('--ip', type=str, required=True, help='目標裝置IP位址', default='192.168.13.240')
    args = parser.parse_args()

    # 執行非同步主程序
    asyncio.run(discover_and_analyze_upnp(args.ip))
