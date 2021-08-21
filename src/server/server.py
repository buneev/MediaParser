import asyncio
from aiohttp import web
import logging

INTERVAL_SECS = 1

async def parse_site(request):
    jo = await request.json()
    cmd = f"cd /code/src && scrapy crawl {jo['spider']} --logfile=/log/{jo['spider']}.log"
    cmd = cmd + f" -a debug={jo.get('debug', False)}"
    pid = await run(cmd)
    logging.info(f'Run web scraping success, PID: {pid}\nCMD: {cmd}')
    return web.json_response(jo)

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()


# async def main():
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
app = web.Application()
app.add_routes([
    web.get('/parse_site', parse_site),
])
web.run_app(app, port=5858)
# return app

