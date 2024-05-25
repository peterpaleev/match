# health_check_server.py
from aiohttp import web
import asyncio

async def handle_health_check(request):
    return web.Response(text="OK")

async def start_server():
    app = web.Application()
    app.router.add_get('/health', handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print("Server started on port 8080. Health check available at /health")
    await asyncio.Event().wait() 

if __name__ == '__main__':
    try:
        asyncio.run(start_server())
    except Exception as e:
        print(f"Error: {e}")

