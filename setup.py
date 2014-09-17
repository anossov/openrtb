from setuptools import setup
import codecs


def readme(fn):
    with codecs.open(fn, encoding='utf-8') as f:
        return f.read()


setup(name='videoamp-openrtb',
      version='0.1.2',
      packages=[
          'openrtb',
      ],
      author='James Wu',
      author_email='james@videoamp.com',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 2.7',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Topic :: Software Development :: Libraries',
      ],
      url='https://github.com/videoamp/openrtb',
      license='BSD',
      description='A set of classes implementing OpenRTB 2.2 and OpenRTB Mobile specifications. Forked form Anossov',
      long_description=readme('README.rst'),
)
