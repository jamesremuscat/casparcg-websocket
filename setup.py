from setuptools import setup, find_packages
import re

VERSIONFILE = "src/casparcg_websocket/_version.py"
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
except EnvironmentError:
    print("unable to find version in %s" % (VERSIONFILE,))
    raise RuntimeError("if %s exists, it is required to be well-formed" % (VERSIONFILE,))

setup(
    name='casparcg_websocket',
    version=verstr,
    description='Bidirectional websocket proxy for CasparCG, supporting both AMCP and OSC',
    author='James Muscat',
    author_email='jamesremuscat@gmail.com',
    url='https://github.com/jamesremuscat/casparcg_websocket',
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir={'': 'src'},
    long_description="""\
    WebSocket proxy for CasparCG, allowing web applications to control CasparCG
    and receive state updates via OSC broadcasts.
    """,
    setup_requires=[],
    tests_require=[],
    install_requires=[
        'autobahn[twisted]',
        'python-dotenv',
        'pythonosc'
    ],
    entry_points={
        'console_scripts': [
            'casparcg-websocket=casparcg_websocket:main'
        ],
    }
)
