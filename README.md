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
2. Install `polyaxon[numpy]==1.1.9` package

```bash
pip install polyaxon[numpy]==1.1.9
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
4. If you don't use git, run `polyaxon init <your-project-name>`. The name should be exactly the same as you provided in the UI. If you use git, run `polyaxon init <your-project-name> --git-url <repo-url> --git-connection repo`

## Experiment Interactively

### Workspace

For the sake of Polyaxon users who do not work with git, a concept of a workspace is introduced. For all the interactive experiments, a `/workspace` path will get populated. Any interactive tool you launch will have `workingDirectory` set to the `/workspace/<project-name>`. These usually also have git installed, so in case you work with git already, you can have your repository checked out there. The content of `/workspace/<project-name>` will not disappear after the environment shutdown.

You can of course still use `POLYAXON_RUN_OUTPUTS_PATH` environment variable to save artifacts under a path recognizable by Polyaxon to be available in the artifacts tab.

### RStudio

Run the following command:

```bash
polyaxon run -f polyaxon/components/rstudio.yml -P theme=Twilight
```

Sample output:

![RStudio run](https://user-images.githubusercontent.com/1897842/95683522-1c4e1a00-0bec-11eb-9b62-8fa2aa85c091.png)

It spawns RStudio service within Polyaxon for your current project. If you don't like the default light theme, you can change it to one of the dark themes. When the link appears, you can simply open it and navigate to the running service embedded within Polyaxon UI, or open it fullscreen (the button in the right upper part).

![Embedded RStudio](https://user-images.githubusercontent.com/1897842/95683545-4ef81280-0bec-11eb-9c5c-47285f2c1e7b.png)

After you launched the RStudio for the first time in the specific workspace, setup your workspace in RStudio with:

```r
packrat::init('.')
```

You can read more about package management with `packrat` [here](https://rstudio.github.io/packrat/walkthrough.html). You need `.Rprofile`, `packrat/init.R`, `packrat/packrat.lock` and `packrat/packrat.opts` in the workspace for a stable definition of working packages used by your scripts.

To run an R experiment in the workspace, just use:

```bash
polyaxon run -f polyaxon/components/r-workspace-experiment.yml -f polyaxon/presets/cpu_medium.yml -P script=<my-script-path> -P args=<my-arguments-as-single-string>
```

If you save your outputs to the directory indicated by the `POLYAXON_RUN_OUTPUTS_PATH` environment variable, they will get versioned and you will be able to access them from the "Artifacts" tab of the experiment (but not from the workspace).

### Visual Studio Code

Run the following command:

```bash
polyaxon run -f polyaxon/components/vscode.yml -P gist=3ad9b36cc07eea65435bc0c13850cc38
```

`gist` parameter may be omitted. It is available for the convenience, as the VS Code has a [Settings Sync](https://marketplace.visualstudio.com/items?itemName=Shan.code-settings-sync) extension pre-installed, that will use your GitHub gist and download your backed up extensions, themes and settings.

Currently, as we are operating in the environment without TLS certificate in place, there may be [issues with copy / paste from the keyboard](https://github.com/cdr/code-server/issues/1566).

### Jupyter Lab

Run the following command:

```bash
polyaxon run -f polyaxon/components/jupyter.yml -P theme="JupyterLab Dark"
```

You can setup the theme as the parameter as it may be annoying to work with light theme by default. You can also specify the exact image to be run, via `-P image=<image-name>` switch.

## Batch Experiments

### Minimal Standalone Python Example

#### Build Environment

Build yourself the environment:

```bash
polyaxon run -f polyaxon/jobs/build.yml -P destination=plx-test:minimal -P dockerfile=docker/base.Dockerfile --git-preset
```

##### Build Explanation

`--git-preset` switch indicates that Polyaxon should clone your repo to to the artifacts path.

The file [`polyaxon/jobs/build.yml`](./polyaxon/jobs/build.yml) declares that the dockerfile [`docker/base.Dockerfile`](./docker/base.Dockerfile) gets built. Finally, the image is tagged `quay.io/kiiaed/plx-test:minimal` and pushed to [`quay.io`](https://quay.io/repository/kiiaed/plx-test?tab=tags).

You can perform any adaptation of the environment within the [`docker/base.Dockerfile`](./docker/base.Dockerfile), commit that and get your environment built. Remember to update the repo / revision.

#### Run the Minimal Standalone Experiment

Run the command:

```bash
polyaxon run -f polyaxon/jobs/minimal.yml --git-preset
```

##### Minimal Standalone Experiment Explanation

Polyaxon downloads `quay.io/kiiaed/plx-test:minimal` image and launches the container with 0.5-1 CPU and 1000-4000MB memory. `--git-preset` switch makes Polyaxon clone the repository that you're in. The container command is simply `python -u -m bin.minimal`.

### DiviK Example

To run the DiviK example with default MSI data, resources allocation and default presets, run the command:

```bash
polyaxon run -f polyaxon/jobs/divik.yml -f polyaxon/presets/cpu_high.yml -f polyaxon/presets/default.yml --git-preset
```

##### DiviK Example Explanation

First, you don't need any build, as DiviK is already provided in the container.

In the [`polyaxon/jobs/divik.yml`](./polyaxon/jobs/divik.yml) you just specify that it should take data from `/data/kiaed01/msi/divik-paper/data.npy`, xy coordinates from `/data/kiaed01/msi/divik-paper/xy.csv` and config from [`config.gin`](./config.gin). These are the most important parameters, that you can track in the repository. You need to reference the full component definition (`pathRef: ../components/divik.yml`, explained below).

[`polyaxon/components/divik.yml`](./polyaxon/components/divik.yml) contains the full component definition that gets pasted at the end of the job definition. It specifies inputs, environment image and all the details of the run. The `fit-clusters` script only saves the files to the expected destination. To track the metric values, data hashes, etc., there's a script [`bin/register_experiment.py`](./bin/register_experiment.py). It gets ran at the end, to provide the full tracking.

[`polyaxon/presets/cpu_high.yml`](./polyaxon/presets/cpu_high.yml) and [`polyaxon/presets/default.yml`](./polyaxon/presets/default.yml) are preset files, that allow you quickly state how much resources your job actually requires (`polyaxon/presets/cpu_high.yml`) or the default values of environment variables (`polyaxon/presets/default.yml`). These are reusable elements that you can always use to patch your environment in regular manner - few more available [here](./polyaxon/presets).

### Random Forest and Grid Search Example

#### Build a Random Forest Environment

Run the following command:

```bash
polyaxon run -f polyaxon/jobs/build.yml -P destination=plx-test:random_forest -P dockerfile=docker/random_forest.Dockerfile --git-preset
```

##### Random Forest Build Explanation

The build works exactly the same as the minimal example, but uses [`docker/random_forest.Dockerfile`](./docker/random_forest.Dockerfile) as an environment definition and pushes the image under different tag ([`quay.io/kiiaed/plx-test:random_forest`](https://quay.io/repository/kiiaed/plx-test?tab=tags)).

In the [`docker/random_forest.Dockerfile`](./docker/random_forest.Dockerfile) you simply indicate that the [`requirements.txt`](./requirements.txt) should get installed, along with package for Polyaxon tracking.

#### Run Random Forest Experiment

Run the following command:

```bash
polyaxon run -f polyaxon/jobs/random_forest.yml -f polyaxon/presets/default.yml -f polyaxon/presets/cpu_low.yml --git-preset -P n_estimators=6 -P min_samples_leaf=120
```

##### Random Forest Experiment Explanation

Runs the [`bin/random_forest.py`](./bin/random_forest.py). In the [`polyaxon/jobs/random_forest.yml`](./polyaxon/jobs/random_forest.yml) we have more inputs and outputs specified. `-P` switch allows to override the default value from the command line.

In the [`bin/random_forest.py`](./bin/random_forest.py) script we have few sections that are dedicated to Polyaxon experiment tracking. It spans data hashes, metric values logging and output model pickle annotation.

Metrics & data details are available in the lineage section:

![Lineage](https://user-images.githubusercontent.com/1897842/95682766-6d0f4400-0be7-11eb-941f-e20f3fa22523.png)

The experiment outputs are available in the artifacts section:

![Artifacts](https://user-images.githubusercontent.com/1897842/95682798-a0ea6980-0be7-11eb-9673-cd37f75013ac.png)

#### Grid Search Run

Run the following command:

```bash
polyaxon run -f polyaxon/jobs/grid_search.yml -f polyaxon/presets/default.yml -f polyaxon/presets/cpu_low.yml --git-preset --eager
```

##### Grid Search Explanation

The [`polyaxon/jobs/grid_search.yml`](./polyaxon/jobs/grid_search.yml) runs the exact same experiment with random forest, but creates several instances of a run, with a different parameterization. `--eager` mode is required for Community Edition of Polyaxon.

### R Experiment

The R experiment follows similar schema as already shown, but packages are managed through `packrat` manager. Therefore build is relatively simple as the packages are installed inplace at the source code location during the runtime. This is to be optimized in the next steps.

#### Build R Environment

Just run the following command:

```bash
polyaxon run -f polyaxon/jobs/build.yml -P destination=plx-test:r -P dockerfile=docker/r.Dockerfile --git-preset
```

It will build and push simplistic R environment to `quay.io/kiiaed/plx-test:r`.

#### Run R Experiment

```bash
polyaxon run -f polyaxon/jobs/iris_r.yml --git-preset
```

##### R Experiment Explanation

The file [`polyaxon/jobs/iris_r.yml`](./polyaxon/jobs/iris_r.yml) refers directly to a premade component with R experiment, discussed below. It points the image `quay.io/kiiaed/plx-test:r`, the R script to run (`bin/iris.R`) and the command line arguments.

The [`polyaxon/components/r-experiment.yml`](./polyaxon/components/r-experiment.yml) firstly restores packages through `packrat`, then executes your selected script with defined arguments. You also need to provide the repo name in the case you are working on your own - this sets up the working directory for the experiment.

You can read more about package management with `packrat` [here](https://rstudio.github.io/packrat/walkthrough.html). You need `.Rprofile`, `packrat/init.R`, `packrat/packrat.lock` and `packrat/packrat.opts` commited to your repository for a stable definition of working packages used by your script.

#### Non-Repo R Experiment

In the case you don't want to create the repository with your code (though that's highly recommended), you can use your Polyaxon workspace as well (discussed already in the interactive experimentation section).

To do this, simply use [`polyaxon/components/r-workspace-experiment.yml`](./polyaxon/components/r-workspace-experiment.yml). It sets your working directory to your workspace, you can reuse all the packages you already had installed there and have the access to all the scripts accessed through RStudio.

Remember: saving to the working directory will create files in the workspace, but these will not be tracked in the artifacts section. To make outputs available in the run artifacts tab, use `POLYAXON_RUN_OUTPUTS_PATH` environment variable to get the required path.
