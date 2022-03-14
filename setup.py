from setuptools import find_packages, setup

setup(
    name="micropy",
    description="Micro Service Infrastructure for Python",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    keywords=["micropy", "micro service", "infrastructure"],
    license="MIT",
    version="0.0.0",
    packages=find_packages(
        include=[
            "micropy",
            "micropy.client",
            "micropy.server",
        ]
    ),
    url="https://github.com/ugatenio/micropy",
    project_urls={
        "Documentation": "",
        "Changes": "https://github.com/ugatenio/micropy/releases",
        "Code": "https://github.com/ugatenio/micropy",
        "Issue tracker": "https://github.com/ugatenio/micropy/issues",
    },
    author="",
    author_email="",
    python_requires=">=3.7",
    install_requires=[
        "rabbitmq>=0.2.0",
        "pika>=1.2.0",
    ],
)
