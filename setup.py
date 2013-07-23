from setuptools import setup
import codecs


def readme(fn):
    with codecs.open(fn, encoding='utf-8') as f:
        return f.read()


setup(name='openrtb',
      version='0.0.6',
      packages=[
          'openrtb',
      ],
      author='Pavel Anossov',
      author_email='anossov@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2.7',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Topic :: Software Development :: Libraries',
      ],
      url='https://github.com/anossov/openrtb',
      license='BSD',
      description='A set of classes implementing OpenRTB 2.0 and OpenRTB Mobile specifications',
      long_description=readme('README.rst'),
)
