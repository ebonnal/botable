from setuptools import setup  # type: ignore

setup(
    name="botable",
    version="1.0.2",
    packages=["botable"],
    url="http://github.com/ebonnal/botable",
    license="Apache 2.",
    author="Enzo Bonnal",
    author_email="bonnal.enzo.dev@gmail.com",
    description="Record and play keyboard and mouse clicks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
