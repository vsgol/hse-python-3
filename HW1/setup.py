import setuptools

setuptools.setup(
    name="astTreeVisualizerGallodest",
    version="1.0.1",
    author="Valery Golovin",
    author_email="galloDest@gmail.com",
    description="AST visualizer.",
    url="https://github.com/vsgol/hse-python-3",
    packages=["astTreeVisualizerGallodest"],
    python_requires=">=3.8",
    install_requires=["networkx==2.6.3", "pydot==1.4.2"],
)
