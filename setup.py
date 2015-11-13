__VERSION__ = '0.0.1'
# import os
import sys
import os
from setuptools import setup, find_packages
from setuptools import Command


install_requires = []
with open('requires.txt', 'r') as fh:
    install_requires = map(lambda s: s.strip(), fh.readlines())

tests_requires = ['unittest2']


readme = []
with open('README.md', 'r') as fh:
    readme = fh.readlines()

class test(Command):
    description = "run the tests"

    user_options = [
        ("test-module=", "m", "Discover tests in specified module"),
        ("test-suite=", "s",
         "Test suite to run (e.g. 'some_module.test_suite')"),
        ("failfast", "f", "Stop running tests on first failure or error")
    ]

    def initialize_options(self):
        self.test_module = None
        self.test_suite = None
        self.failfast = False

    def finalize_options(self):
        if self.test_suite is None and self.test_module is None:
            self.test_module = 'test'
        elif self.test_module is not None and self.test_suite is not None:
            raise DistutilsOptionError(
                "You may specify a module or suite, but not both"
            )

    def run(self):
        # Installing required packages, running egg_info and build_ext are
        # part of normal operation for setuptools.command.test.test
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "natr.settings")

        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(
                self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)
        self.run_command('egg_info')
        # build_ext_cmd = self.reinitialize_command('build_ext')
        # build_ext_cmd.inplace = 1
        # self.run_command('build_ext')

        # Construct a TextTestRunner directly from the unittest imported from
        # test (this will be unittest2 under Python 2.6), which creates a
        # TestResult that supports the 'addSkip' method. setuptools will by
        # default create a TextTestRunner that uses the old TestResult class,
        # resulting in DeprecationWarnings instead of skipping tests under 2.6.
        from test import unittest, test_cases
        if self.test_suite is None:
            all_tests = unittest.defaultTestLoader.discover(self.test_module)
            suite = unittest.TestSuite()
            suite.addTests(sorted(test_cases(all_tests),
                                  key=lambda x: x.__module__))
        else:
            suite = unittest.defaultTestLoader.loadTestsFromName(
                self.test_suite)
        result = unittest.TextTestRunner(
            verbosity=2, failfast=self.failfast).run(suite)
        sys.exit(not result.wasSuccessful())


# class RunTests(Command):
#     """From django-celery"""
#     description = "Run the django test suite from the tests dir."
#     user_options = []
#     extra_env = {}

#     def run(self):
#         if self.distribution.install_requires:
#             self.distribution.fetch_build_eggs(
#                 self.distribution.install_requires)
#         if self.distribution.tests_require:
#             self.distribution.fetch_build_eggs(self.distribution.tests_require)

#         for env_name, env_value in self.extra_env.items():
#             os.environ[env_name] = str(env_value)

#         this_dir = os.getcwd()
#         testproj_dir = os.path.join(this_dir, 'synplan')
#         os.chdir(testproj_dir)
#         sys.path.append(testproj_dir)

#         os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get(
#             'DJANGO_SETTINGS_MODULE', 'synplan.settings')
#         os.environ['DJANGO_CONFIGURATION'] = os.environ.get(
#             'DJANGO_CONFIGURATION', 'TestSettings')

#         from configurations.management import execute_from_command_line
#         execute_from_command_line([__file__, 'test'])

#     def initialize_options(self):
#         pass

#     def finalize_options(self):
#         pass

setup(
    name='natr',
    version=__VERSION__,
    author='xepa4ep',
    author_email='r.kamun@gmail.com',
    url='https://github.com/Mafioso/natr',
    description='',
    long_description=''.join(readme),
    packages=find_packages(),
    zip_safe=True,
    install_requires=install_requires,
    tests_require=tests_requires,
    # extras_require={'test': tests_requires},
    cmdclass={"test": test},
    include_package_data=True,
    # entry_points={
    #     'console_scripts': [
    #         'ko = src.runner:entry_point'
    #     ]
    # },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Tornado',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2.7'
    ]
)