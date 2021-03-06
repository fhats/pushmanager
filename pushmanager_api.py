#!/usr/bin/python
from __future__ import with_statement
import os
import tornado.httpserver
import tornado.process

from core.application import Application
import core.db as db
from core.settings import Settings
from core.util import get_servlet_urlspec
from servlets.api import APIServlet
import ui_modules

api_application = tornado.web.Application(
    # Servlet dispatch rules
    [
        get_servlet_urlspec(APIServlet),
    ],
    # Server settings
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    gzip = True,
    login_url = "/login",
    cookie_secret = Settings['cookie_secret'],
    ui_modules = ui_modules,
    autoescape = None,
)

class PushManagerAPIApp(Application):
    name = "api"

    def start_services(self):
        # HTTP server (for api)
        sockets = tornado.netutil.bind_sockets(self.port, address=Settings['api_app']['servername'])
        tornado.process.fork_processes(0)
        server = tornado.httpserver.HTTPServer(api_application)
        server.add_sockets(sockets)

if __name__ == '__main__':
    app = PushManagerAPIApp()
    db.init_db()
    app.run()
