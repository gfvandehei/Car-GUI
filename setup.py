from setuptools import setup, find_packages

setup(
   name='JeepGUI',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['lib'],  #same as name
   install_requires=['dependency_injector'], #external packages as dependencies
)