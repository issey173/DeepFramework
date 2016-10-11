import setuptools

import dframe


def get_dependencies():
    with open('requirements.txt', 'r') as f:
        dependencies = list(f)
        dependencies = [dependency.replace('\n', '') for dependency in dependencies]
        return dependencies


setuptools.setup(
    name='DeepFramework',
    version=dframe.__version__,
    description='Python framework for Deep Learning',
    url='https://github.com/issey173/deepframework.git',
    author='Issey Masuda Mora',
    author_email='issey173@gmail.com',
    license='MIT',
    packages=['dframe'],
    install_requires=get_dependencies(),
    zip_safe=False
)
