from distutils.core import setup

setup(name='pyXDSM',
      version='2.0.0',
      description="Python script to generate PDF XDSM diagrams using TikZ and LaTeX",
      long_description="""\
      """,
      classifiers=[
      ],
      keywords='optimization multidisciplinary multi-disciplinary analysis n2 xdsm',
      author='',
      author_email='',
      url='http://mdolab.engin.umich.edu/',
      license='Apache License, Version 2.0',
      packages=[
          'pyxdsm',
      ],
      package_data={
          'pyxdsm': ['*.tex']
      },
      install_requires=[
            'numpy>=1.9.2'
      ])
