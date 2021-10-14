from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kgcl",
    version="0.0.10",
    description="Knowledge Graph Change Language",
    packages=[
        "kgcl.apply",
        "kgcl.diff",
        "kgcl.grammar",
        "kgcl.model",
    ],
    # py_modules=[
    #    "kgcl",
    #    "kgcl_diff",
    #    "pretty_print_kgcl",
    # ],
    package_dir={"kgcl": "./kgcl"},
    package_data={"kgcl.grammar": ["kgcl.lark"]},
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "linkml ~= 1.0.3",
        "lark ~= 0.11.3",
    ],
    extras_require={"dev": ["pytest>=3.7"]},
    url="https://github.com/ckindermann/knowledge-graph-change-language",
    author="Christian Kindermann",
    author_email="chris.kind.man@gmail.com",
),
