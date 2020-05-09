import os
from asyncio import sleep
from notebook.base.handlers import IPythonHandler

class XarrayLeafletHandler(IPythonHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'image/png')
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

    async def get(self, path):
        path = '/' + path
        tile_done = path[:-4] + '.done'
        delete = False
        timeout = False
        dt = 0.1
        t = 0
        while True:
            if os.path.exists(tile_done):
                with open(tile_done) as f:
                    txt = f.read()
                if txt.startswith('keep'):
                    break
                elif txt.startswith('delete'):
                    delete = True
                    break
            await sleep(dt)
            t += dt
            # don't wait more than one second
            # Leaflet can make a request while dragging but Python is not
            # triggered unless the mouse button is released, so the file
            # will never be written
            if t > 1:
                timeout = True
                break
        if not timeout:
            with open(path, 'rb') as f:
                tile = f.read()
            if delete:
                os.remove(tile_done)
                os.remove(path)
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.finish(tile)


#from jupyter_server.base.handlers import JupyterHandler
#import tornado
#from time import sleep
#
#
#class XarrayLeafletHandler(JupyterHandler):
#
#    @tornado.web.authenticated
#    async def get(self, path):