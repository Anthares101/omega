from setuptools import setup, find_packages

setup(
    name='omega_wp',
    version='2.5.post4',
    license='GPL-2.0',
    description='From Wordpress admin to pty automatically!',
    author='Ángel Heredia',
    packages=find_packages(),
    url='https://github.com/anthares101/omega',
    keywords='windows macos linux shell wordpress reverse-shell tool hacking tty pty cybersecurity reverse pwntools hacktoberfest kali',
    python_requires='>=3',
    install_requires=[
        'pwntools',
        'requests',
        'bs4',
        'lxml'
    ],
    extras_require={
        'dev': [
            'responses',
        ]
    },
    entry_points='''
        [console_scripts]
        omega=omega_wp.__main__:main
    ''',
)
