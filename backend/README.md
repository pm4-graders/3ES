## How to start the backend
1. Set the PYTHONPATH environment variable: You can set this variable in a few different ways, depending on your operating system and how you want to set the variable.

In <strong>Linux</strong> and macOS, you can set the PYTHONPATH variable in your shell by running the following command in your terminal:</br>
This command adds your project path to the beginning of the PYTHONPATH variable, so that Python will search your project directory first when it tries to import modules.

<code>export PYTHONPATH=/path/to/your/project:$PYTHONPATH</code>


In <strong>Windows</strong>, you can set the PYTHONPATH variable by following these steps:

a) Open the Start menu and search for "Environment Variables".</br>
b) Click on "Edit the system environment variables".</br>
c) Click on the "Environment Variables" button at the bottom of the "System Properties" window.</br>
d) Under "System Variables", click on the "New" button and enter PYTHONPATH as the variable name and the path to your project as the variable value.

2. To start the backend navigate to the app directory and use the command `uvicorn main:app --reload`
