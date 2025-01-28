import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_shoppingcart",
    version="0.1.7",
    author="Brixt18",
    author_email="",
    description="Add a shopping cart to your Flask app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Brixt18/flask-shoppingcart",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Typing :: Typed",
    ],
)