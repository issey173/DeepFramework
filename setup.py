import setuptools

import dframe

setuptools.setup(
    name='DeepFramework',
    version=dframe.__version__,
    description='Python framework for Deep Learning',
    long_description='DeepFramework is an abstract layer designed to be on top of any of your deep learning projects. '
                     'This framework intends to provide a layer to separate your models logic '
                     '(what is actually training, predicting...) from all the scripting needed to execute that, '
                     'so that you can encapsulate and separate the core of your program from everything else. '
                     'With that you can actually focus on designing your architecture and forget about all the '
                     'surrounding boilerplate, and what it\'s more important, it will speed up your prototyping and '
                     'the scaffolding of your project.',
    url='https://github.com/issey173/deepframework.git',
    author='Issey Masuda Mora',
    author_email='issey173@gmail.com',
    license='MIT',
    packages=['dframe', 'dframe.dataset', 'dframe.model', 'dframe.pipeline'],
    install_requires=[
        'numpy>=1.11.1',
        'h5py>=2.6.0',
        'six>=1.10.0'
    ],
    zip_safe=False
)
