import asyncio
from aiohttp import web
import logging
from settings import * 
import os


async def parse(request):
    ''' запуск процесса парсинга '''
    jo = await request.json()
    if DEBUG:
        path = 'cd ../ && '
    else:
        path = 'cd /code/src && '

    sp_name = jo.get('spider_name', '')
    cmd = f"{path}scrapy crawl {sp_name} -o data/{sp_name}.json --logfile=data/log/{sp_name}.log"

    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    
    # logger.info(f'{cmd!r} Exited with {proc.returncode}')
    # stdout, stderr = await proc.communicate()
    # text = ''
    # status = ''
    # if stdout:
    #     text = stdout.decode()
    #     logger.info(f"[stdout] {text}")
    #     status = 'success'
    # if stderr:
    #     text = stderr.decode()
    #     logger.error(f"[stderr] {text}")
    #     status = 'error'
    # return web.json_response({'success': status, 'text': text})
    return web.json_response({'success': 'true'})


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.post('/run_parse', parse)
    ])
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger("[scrapy]")
    web.run_app(app, port=5858)

