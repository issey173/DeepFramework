import setuptools

import dframe

setuptools.setup(
    name='DeepFramework',
    version=dframe.__version__,
    description='Python framework for Deep Learning',
    url='https://github.com/issey173/deepframework.git',
    author='Issey Masuda Mora',
    author_email='issey173@gmail.com',
    license='MIT',
    packages=['dframe'],
    install_requires=[
        'h5py==2.6.0',
        'numpy==1.11.1',
        'six==1.10.0'
    ],
    zip_safe=False
)
