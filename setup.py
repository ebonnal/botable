from setuptools import setup  # type: ignore

setup(
    name="botable",
    version="0.0.10",
    packages=["botable"],
    url="http://github.com/ebonnal/botable",
    license="Apache 2.",
    author="Enzo Bonnal",
    author_email="bonnal.enzo.dev@gmail.com",
    description="Record and play keyboard and mouse events",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["pynput==1.7.7"],
        entry_points={
        "console_scripts": [
            "botable=botable.__main__:main",
        ],
    },
)
