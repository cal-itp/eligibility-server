from setuptools import find_packages, setup


with open("requirements.txt") as f:
    requirements = f.read().strip().split("\n")
    install_requires = [r for r in requirements if not r.startswith("git+")]
    dependency_links = list(set(requirements) - set(install_requires))

with open("README.md") as f:
    long_description = f.read()


CLASSIFIERS = [
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
]

setup(
    name="eligibility-server",
    version="2022.12.1",
    description="Server implementation of the Eligibility Verification API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=CLASSIFIERS,
    project_urls={
        "Source": "https://github.com/cal-itp/eligibility-server",
        "Tracker": "https://github.com/cal-itp/eligibility-server/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    license="AGPL-3.0",
)
