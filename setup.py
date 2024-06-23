from setuptools import find_packages, setup

setup(
    name="raulito_run",
    version="0.1.0",
    description="very simple 2D jump game",
    author="Jose Machado",
    author_email="m4ch4do@protonmail.com",
    url="https://github.com/jm4ch4do/py_game_mario",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pygame>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "my_pygame_game = scenes.level_001",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
