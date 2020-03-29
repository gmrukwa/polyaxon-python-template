# Polyaxon Python Template

Template repository to use Polyaxon in Python within Silesian University of Technology infrastructure

## Repository Structure

```plaintext
|- .gitignore               # List of all files that should not be tracked via git
|- .polyaxonignore          # List of all files that should not be uploaded to Polyaxon
```

## How to Start

### First Time Setup

Skip this if you already used Polyaxon for another project.

1. Contact Polyaxon administrator to create an account for you.
2. Make `polyaxon.aei.polsl.pl` recognized from your computer. Open the following file in editable mode:
  - Windows: `C:\Windows\System32\Drivers\etc\hosts`
  - UNIX: `/etc/hosts`
and create following entry at the end of the file:

```plaintext
157.158.109.238 polyaxon.aei.polsl.pl
```

3. Install `polyaxon-cli==0.6.1` package

```bash
pip install polyaxon-cli==0.6.1
```

4. Connect to VPN.
5. Login to your account [here](http://polyaxon.aei.polsl.pl/users/login/).
6. Setup your Polyaxon CLI installation. Run in command line:

```bash
polyaxon config set --host=polyaxon.aei.polsl.pl --port=80
```

7. Login to your Polyaxon account with CLI. Run in command line:

```bash
polyaxon login
```

You will be asked if the webpage should be opened. Confirm with `y` and copy the token to the clipboard. Paste the token into command line (no characters will appear) and confirm with `Enter`.

### New Project Setup

The steps below assume that you are connected to VPN. We will remove this restriction soon but due to technical reasons it's not possible at the moment. Also, you need to be logged in to the Polyaxon dashboard.

**Important:** *These steps are required for anyone working on the same project, as the project in Polyaxon is tied to a specific user.*

1. Open the [Polyaxon dashboard](http://polyaxon.aei.polsl.pl/app/)
2. Create new project in the UI:

![Create new project](https://user-images.githubusercontent.com/1897842/77849332-32a20480-71cb-11ea-973d-7ca3e60c4164.png)

2. Open command line
3. Navigate to the project directory on your computer
4. Run `polyaxon init <your-project-name>`. The name should be exactly the same as you provided in the UI.
5. Make sure no big files are present in the project directory. If there are, list them in `.polyaxonignore` file. For data transfer please contact the Polyaxon admin at the moment. This stage is under construction to be more convenient and efficient.
6. Run `polyaxon upload` to upload code files.
7. Run `pip install -r requirements.txt` to install locally all the requirements, so you can debug your code locally. Please remember about the [proper dependencies management](https://www.kennethreitz.org/essays/a-better-pip-workflow) and environment isolation via [`venv`](https://docs.python.org/3/tutorial/venv.html) or `conda`.

Now you can schedule experiments and play with notebooks.

You can conduct all the above steps with Command Line Interface as well. More about this [here](https://docs.polyaxon.com/references/polyaxon-cli/project/).
