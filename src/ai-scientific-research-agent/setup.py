from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="sci_research_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=Path("requirements.txt").read_text().splitlines(),
    python_requires=">=3.12",
    description="AI to write shitty scientific research papers",
    author="Alex Galea",
    author_email="agalea91@gmail.com",
    url="https://github.com/zazencodes/zazencodes-season-2/src/ai-scientific-research-agent",
    license="MIT",
)
