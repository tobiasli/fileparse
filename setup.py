import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='fileparse-tobiasli',
                 version='1.0.2',
                 description='Package for converting string timestamps into datetimes.',
                 author='Tobias Litherland',
                 author_email='tobiaslland@gmail.com',
                 url='https://github.com/tobiasli/fileparse',
                 packages=setuptools.find_packages(),
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 install_requires=['pytest']
                 )
