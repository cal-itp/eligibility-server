from setuptools import setup

setup(
    name="eligibility_server",
    packages=["eligibility_server"],
    include_package_data=True,
    install_requires=[
        "flask",
    ],
)
