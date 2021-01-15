from __future__ import absolute_import
#from distutils.core import setup
from setuptools import setup

descr = """Tree representations and algorithms for Python.

Viridis is named after the green tree python, Morelia viridis.
"""

DISTNAME            = 'viridis'
DESCRIPTION         = 'Tree data structures and algorithms'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Juan Nunez-Iglesias'
MAINTAINER_EMAIL    = 'juan.nunez-iglesias@monash.edu'
URL                 = 'https://github.com/jni/viridis'
LICENSE             = 'BSD 3-clause'
DOWNLOAD_URL        = 'https://github.com/jni/viridis'
VERSION             = '0.5.0'
PYTHON_VERSION      = (3, 5)
INST_DEPENDENCIES   = []


if __name__ == '__main__':

    setup(name=DISTNAME,
        version=VERSION,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        license=LICENSE,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
        ],
        packages=['viridis'],
        package_data={},
        install_requires=INST_DEPENDENCIES,
        scripts=[]
    )

