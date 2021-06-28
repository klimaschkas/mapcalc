import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name='mapcalc',
  packages=['mapcalc'],
  version='0.2.2',
  license='apache-2.0',
  description='Calculates the mAP value in object detection tasks',
  author='Simon Klimaschka',
  author_email='simon.klimaschka@gmail.com',
  url='https://github.com/LeMuecke/mapcalc',
  download_url='https://github.com/LeMuecke/mapcalc/archive/v_0.2.2-beta.tar.gz',
  keywords=['object detection', 'map', 'mean average precision'],
  long_description=long_description,
  long_description_content_type="text/markdown",
  install_requires=[
          'numpy',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)