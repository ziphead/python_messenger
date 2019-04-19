from functools import reduce
from settings import INSTALLED_MODULES


def get_server_routes():
    return reduce(
        lambda routes, module: routes + getattr(module, 'routes', []),
        reduce(
            lambda submodules, module: submodules + [getattr(module, 'routes', [])],
            reduce(
                lambda modules, module: modules + [__import__(f'{module}.routes')],
                INSTALLED_MODULES,
                []
            ),
            []
        ),
        []
    )


def resolve(action, routes=None):
    print(routes)
    routes_mapping = {
        route.get('action'): route.get('controller')
        for route in routes or get_server_routes()
    }
    return routes_mapping.get(action, None)
