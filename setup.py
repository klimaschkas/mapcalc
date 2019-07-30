from distutils.core import setup
setup(
  name='mapcalc',
  packages=['mapcalc'],
  version='0.1',
  license='apache-2.0',
  description='Calculates the mAP value in object detection tasks',
  author='Simon Klimaschka',
  author_email='simon.klimaschka@gmail.com',
  url='https://github.com/LeMuecke/mapcalc',
  download_url='https://github.com/LeMuecke/mapcalc/archive/v_0.1-beta.tar.gz',
  keywords=['object detection', 'map', 'mean average precision'],
  install_requires=[
          'numpy',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache 2.0',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)