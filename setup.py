"""Setup awspds-mosaic."""

from setuptools import setup, find_packages


# Runtime requirements.
inst_reqs = [
    "lambda-proxy-cache",
    "loguru",
    "mercantile",
    "Pillow",
    "rio-color",
    "rio_tiler>=1.2.7",
    "rio_tiler_mosaic>=0.0.1dev3",
    "requests",
    "supermercado",
    "shapely",
]
extra_reqs = {
    "test": ["pytest", "pytest-cov", "mock"],
    "dev": ["pytest", "pytest-cov", "pre-commit", "mock"],
}

setup(
    name="awspds-mosaic",
    version="0.0.1",
    description=u"Create and serve mosaics.",
    long_description=u"Create and serve mosaics.",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="COG GIS",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points={"console_scripts": ["awspds-mosaic = awspds_mosaic.scripts.cli:run"]},
)
