from setuptools import setup

version = '1.0.2'

requirements = [
    'ftransc==6.0.10',
    'PyQt5',
    'nose',
]


if 'a' in version:
    dev_status = '3 - Alpha'
elif 'b' in version:
    dev_status = '4 - Beta'
else:
    dev_status = '5 - Production/Stable'

setup_args = {
    'name': 'ftransc_gui',
    'version': version,
    'author': 'Mkhanyisi Madlavana',
    'author_email': 'mkhanyisi@gmail.com',
    'url': 'https://github.com/dopstar/ftransc-gui',
    'download_url': 'https://github.com/dopstar/ftransc-gui/tarball/{0}'.format(version),
    'package_dir': {'ftransc_gui': 'ftransc_gui'},
    'description': 'The GUI application for ftransc',
    'long_description': 'The GUI application for ftransc',
    'packages': [
        'ftransc_gui',
    ],
    'package_data': {'ftransc_gui': ['*.md']},
    'install_requires': requirements,
    'keywords': 'ftransc, gui, audio, convert, ffmpeg, avconv, mp3, wma, ogg, flac, transcode',
    'classifiers': [
        'Development Status :: {0}'.format(dev_status),
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    'entry_points': {
        'console_scripts': [
            'ftransc-gui=ftransc_gui.launcher:gui',
        ]
    }
}

setup(**setup_args)
