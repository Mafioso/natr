__VERSION__ = '1.0.59'
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

class RunTests(Command):
    """From django-celery"""
    description = "Run the django test suite from the tests dir."
    user_options = []
    extra_env = {}

    def run(self):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(
                self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        for env_name, env_value in self.extra_env.items():
            os.environ[env_name] = str(env_value)

        os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get(
            'DJANGO_SETTINGS_MODULE', 'natr.settings')
        os.environ['DJANGO_CONFIGURATION'] = os.environ.get(
            'DJANGO_CONFIGURATION', 'TestSettings')


        from django.core.management import execute_from_command_line
        execute_from_command_line([__file__, 'test'])

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


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
    cmdclass={"test": RunTests},
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
