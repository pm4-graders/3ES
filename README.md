# 3ES




## Installation (openCV / venv)
We should be using virtual environments to not have problems with other versions of python etc.

1. Download Anaconda for Windows: https://www.anaconda.com/products/distribution#Downloads, add to PATH
2. Run 'conda create --name virtualenv python=3.8'
3. 'conda activate virtualenv'
4. 'pip install opencv-contrib-python'

To deactivate the virtual environment: 'conda deactivate'

## Use anaconda with vscode

1. Ctrl+Shift+P -> Enter "Python: Select Interpreter"
2. Select the virtualenv you just created.