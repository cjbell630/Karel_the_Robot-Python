import os
import pathlib
import sys
from shutil import rmtree

from setuptools import setup, Command

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        """self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')"""

        sys.exit()


# This call to setup() does all the work
setup(
    name="karel_the_robot",  # what will be typed when you use pip install
    version="1.1.0",
    description="Unofficial port of Karel the Robot to Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cjbell630/Karel_the_Robot-Python",
    author="Connor Bell",
    author_email="ronnoclleb@gmail.com",
    packages=["karel_the_robot"],  # what will be typed when you use import
    package_dir={"karel_the_robot": "karel_the_robot/src"},
    include_package_data=True,
    install_requires=["numpy", "pygame", "sentry_sdk"],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
