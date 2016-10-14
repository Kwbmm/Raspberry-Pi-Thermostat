#!/usr/bin/env python

import web
from routes.Home import Home
from routes.Program import Program
from routes.Login import Login

urls = (
    "/", "Home",
    "/program/(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", "Program",
    "/login", "Login"
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
