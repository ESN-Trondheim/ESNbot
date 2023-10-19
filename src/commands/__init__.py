import pkgutil

# This will dynamically import all modules in this directory
# which makes them accessible via the commands package, f.ex:
# import commands.help
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module