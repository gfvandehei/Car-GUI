import sys
import os
import importlib.util as imp
import inspect

class AppController(object):

    def __init__(self, applications="./lib/app/gui/apps"):
        self.app_path = applications
        if not os.path.exists(applications):
            raise(OSError("No app directory {} exists".format(applications)))
        self.app_list = os.listdir(self.app_path)
        self.app_modules = {}
        print("loading", self.app_list)
        self.load_apps()

    def load_apps(self):
        for file_name in self.app_list:
            if file_name.find('_') == -1:
                spec = imp.spec_from_file_location(file_name[0:-3], self.app_path+"/"+file_name)
                print(spec)
                module = imp.module_from_spec(spec)
                spec.loader.exec_module(module)
                members = inspect.getmembers(module, inspect.isclass)
                print(members)
                self.app_modules[members[0][0]] = members[0][1]
        print(self.app_modules)

    def get_app_names(self):
        return list(self.app_modules.keys())
    
    def get_app_list(self):
        return list(self.app_modules)