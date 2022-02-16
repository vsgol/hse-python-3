FROM python:3.9
COPY src/latex_utils.py src/latex_utils.py
RUN apt-get update
RUN apt-get install texlive-latex-base texlive-lang-cyrillic graphviz -y
RUN python3.9 -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple astTreeVisualizerGallodest==1.0.1
RUN python3.9 src/latex_utils.py

WORKDIR artifacts
RUN pdflatex file.tex
RUN rm file.aux file.log