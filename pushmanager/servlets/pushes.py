import pushmanager.core.util
import tornado.gen
import tornado.web
from pushmanager.core.requesthandler import RequestHandler


class PushesServlet(RequestHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        pushes_per_page = pushmanager.core.util.get_int_arg(self.request, 'rpp', 50)
        before = pushmanager.core.util.get_int_arg(self.request, 'before', 0)
        push_user = pushmanager.core.util.get_str_arg(self.request, 'user', '')
        state = pushmanager.core.util.get_str_arg(self.request, 'state', '')
        response = yield tornado.gen.Task(
                        self.async_api_call,
                        'pushes',
                        {
                            'rpp': pushes_per_page,
                            'before': before,
                            'user': push_user,
                            'state': state,
                        }
                    )

        results = self.get_api_results(response)
        if not results:
            self.finish()

        pushes, last_push = results
        self.render(
            "pushes.html",
            page_title="Pushes",
            pushes=pushes,
            rpp=pushes_per_page,
            push_user=push_user,
            state=state,
            last_push=last_push
        )
