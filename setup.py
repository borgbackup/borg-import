# -*- encoding: utf-8 *-*
import sys

min_python = (3, 4)
my_python = sys.version_info

if my_python < min_python:
    print("borg-import requires Python %d.%d or later" % min_python)
    sys.exit(1)


from setuptools import setup, find_packages


with open('README.rst', 'r') as fd:
    long_description = fd.read()


setup(
    name='borg-import',
    use_scm_version={
        'write_to': 'src/borg_import/_version.py',
    },
    author='The Borg Collective (see AUTHORS file)',
    author_email='borgbackup@python.org',
    url='https://borgimport.readthedocs.io/',
    description='Import backups made with misc. other software into borgbackup',
    long_description=long_description,
    license='BSD',
    platforms=['Linux', ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Archiving :: Backup',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'borg-import = borg_import.main:below_main',
        ]
    },
    setup_requires=['setuptools_scm>=1.7', ],
    install_requires=[],
)
