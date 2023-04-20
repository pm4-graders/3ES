# 3ES

[![GitHub Issues](https://img.shields.io/github/issues/pm4-graders/3ES.svg)](https://github.com/pm4-graders/3ES/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/pm4-graders/3ES.svg?style=flat-square)](https://github.com/pm4-graders/3ES/pulls)
![GitHub last commit](https://img.shields.io/github/last-commit/pm4-graders/3ES)
![GitHub contributors](https://img.shields.io/github/contributors/pm4-graders/3ES)

![GitHub language count](https://img.shields.io/github/languages/count/pm4-graders/3ES)
![GitHub top language](https://img.shields.io/github/languages/top/pm4-graders/3ES)

![GitHub repo file count](https://img.shields.io/github/directory-file-count/pm4-graders/3ES)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/pm4-graders/3ES)
[![Stargazers](https://img.shields.io/github/stars/pm4-graders/3ES.svg)](https://github.com/pm4-graders/3ES/stargazers)





## Installation (openCV / venv)
We should be using virtual environments to not have problems with other versions of python etc.

1. Download Anaconda for Windows: https://www.anaconda.com/products/distribution#Downloads, add to PATH
2. Run 'conda create --name virtualenv python=3.8'
3. conda activate virtualenv
4. pip install opencv-contrib-python
5. pip3 install torch torchvision torchaudio
6. pip install keras
7. pip install tensorflow

To deactivate the virtual environment: 'conda deactivate'

## Use anaconda with vscode

1. Ctrl+Shift+P -> Enter "Python: Select Interpreter"
2. Select the virtualenv you just created.