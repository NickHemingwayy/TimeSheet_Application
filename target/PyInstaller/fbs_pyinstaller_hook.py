import importlib
module = importlib.import_module('fbs_runtime._frozen')
module.BUILD_SETTINGS = {'app_name': 'Test', 'author': 'Nick', 'version': '0.0.0', 'environment': 'local'}