from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Getting data from vk.com pythonic and easily.'
LONG_DESCRIPTION = 'A package that allows to get data from groups in vk.com in just few lines of code.'

# Setting up
setup(
    name="vk_getter",
    version=VERSION,
    author="Crawlic (Nikita Kuznetsov)",
    author_email="nikitosik0726@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'vk', 'api', 'data', 'image', 'posts', 'vk get'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)