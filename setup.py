import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='kegg',
    version='0.0.0',
    author='Anmol Gorakshakar',
    author_email='gorakshakar.a@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/',  # github repository URL
    license='MIT',  # license type
    install_requires=['requests']
)
