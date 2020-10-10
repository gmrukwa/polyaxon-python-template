# Polyaxon Python Template

Template repository to use Polyaxon in Python within Silesian University of Technology infrastructure

## Repository Structure

```plaintext
|- .gitignore                   # Lists all files not tracked via git
|- .polyaxonignore              # Lists all files not uploaded to Polyaxon
|- bin                          # Executable scripts for your experiments
|  |- __init__.py
|  |- ...
|  \- minimal.py                # Some experiment script
|- my_project                   # Reusable components of your current project, shared between the scripts
|  |- __init__.py
|  |- ...
|  \- data.py                   # Module for easy data access
|- notebooks                    # Jupyter Notebooks you use for exploration / data review
|  |- quickstart.ipynb          # Initial observations about the data characteristics
|  |- ...
|  \- random_forest.ipynb       # Some advanced analysis of results
|- polyaxon                     # Common place for polyaxonfiles
|  |- minimal.yml               # Some experiment
|  |- ...
|  \- other.yml
|- requirements-to-freeze.txt   # Direct dependencies for your experiments
\- requirements.txt             # All the pinned packages versions (from pip freeze)
```

## How to Start

### First Time Setup

Skip this if you already used Polyaxon for another project.

1. Contact Polyaxon administrator to create VPN configuration for you.
2. Install `polyaxon-cli==1.1.9` package

```bash
pip install polyaxon-cli==1.1.9
```

3. Connect to VPN.
4. Setup your Polyaxon CLI installation. Run in command line:

```bash
polyaxon config set --host=http://polyaxon-polyaxon-gateway.polyaxon.svc.cluster.local:80
```

### New Project Setup

The steps below assume that you are connected to VPN.

1. Open the [Polyaxon dashboard](http://polyaxon-polyaxon-gateway.polyaxon.svc.cluster.local/)
2. Create new project in the UI:

![Create new project](https://user-images.githubusercontent.com/1897842/77849332-32a20480-71cb-11ea-973d-7ca3e60c4164.png)

2. Open command line
3. Navigate to the project directory on your computer
4. Run `polyaxon init <your-project-name>`. The name should be exactly the same as you provided in the UI.


```bash
polyaxon run -f polyaxon/jobs/build_minimal.yml
```

```bash
polyaxon run -f polyaxon/jobs/minimal.yml --git-preset
```

```bash
polyaxon run -f polyaxon/jobs/build_random_forest.yml
```

```bash
polyaxon run -f polyaxon/jobs/random_forest.yml -f polyaxon/presets/default.yml -f polyaxon/presets/cpu_low.yml --git-preset
```

```bash
polyaxon run -f polyaxon/jobs/grid_search.yml -f polyaxon/presets/default.yml -f polyaxon/presets/cpu_low.yml --git-preset --eager
```

```bash
polyaxon run -f polyaxon/jobs/build_r.yml --git-preset
```

```bash
polyaxon run -f polyaxon/jobs/iris_r.yml --git-preset
```

```bash
polyaxon run -f polyaxon/components/vscode.yml -P gist=3ad9b36cc07eea65435bc0c13850cc38
```

```bash
polyaxon run -f polyaxon/components/rstudio.yml -P theme=Twilight
```

```bash
polyaxon run -f polyaxon/components/jupyter.yml -P theme="JupyterLab Dark"
```


6. Run `polyaxon upload` to upload code files.
7. Run `pip install -r requirements.txt` to install locally all the requirements, so you can debug your code locally. Please remember about the [proper dependencies management](https://www.kennethreitz.org/essays/a-better-pip-workflow) and environment isolation via [`venv`](https://docs.python.org/3/tutorial/venv.html) or `conda`.

Now you can schedule experiments and play with notebooks.

You can conduct all the above steps with Command Line Interface as well. More about this [here](https://docs.polyaxon.com/references/polyaxon-cli/project/).

## Run Experiment

Select one of the files under `polyaxon` directory and run it like:

```bash
polyaxon run -u -f polyaxon/minimal.yml
```

You can find your experiment / experiment group in the dashboard.

More details about:

- `polyaxon run` command can be found [here](https://docs.polyaxon.com/references/polyaxon-cli/run/).
- concepts in Polyaxon (experiment, experiment group, job, etc.) can be found [here](https://docs.polyaxon.com/concepts/architecture/#polyaxon-concepts)
- how to work with [the experiment](https://docs.polyaxon.com/concepts/experiments/), [the experiment group](https://docs.polyaxon.com/concepts/experiment-groups-hyperparameters-optimization/)
- [polyaxonfile specification](https://docs.polyaxon.com/references/polyaxonfile-yaml-specification/)
- [how to disable Polyaxon tracking without changing the code for local experiments](https://docs.polyaxon.com/references/polyaxon-tracking-api/#disabling-polyaxon-tracking-without-changing-the-code)
- [how to track experiments](https://docs.polyaxon.com/references/polyaxon-tracking-api/experiments/)

## Experiment Interactively

You need to create a polyaxonfile specifying the notebook session and run it like:

```bash
polyaxon notebook start -u -f polyaxon/notebook.yml
```

It takes up to few minutes to build the environment and you can start playing.

Keep in mind that after stopping the notebook, all your progress will be **lost**. Therefore you need to **download** the notebook with your results to the `notebooks` directory.

Finally, remember to `polyaxon notebook stop` at the end, otherwise you will keep resources blocked for everyone.
