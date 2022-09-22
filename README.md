# Reading Timeline

Visualise your readings with an automatically generated timeline.

<p align="center">
	<img src="timeline.svg" height="1000">
</p>

## Getting Started

Reading Timeline is intended to work without the need to access or modify the source code. To generate the timeline, there are some parameters that are described in the following files:

- `data.yml`. Contains the actual book data. Categories, books, and all of their properties.
- `config.yml`. Contains the parameters used to generate the drawing. For example: the color of the timeline, the width of its line, the font of the labels, etc.

These files should be self-explanatory, so feel free to play around to fully  customise your timeline.

Further explanation on how the program works will soon be available on [my website](https://www.albertcanales.com)

## Prerequisites

The program can be run on all operating systems. The prerequisites are:

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Used in recommended installation but not required
- [Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [VirtualEnv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv)

For now, the tool is installed and used as a CLI application, so some basic terminal usage will be needed.

## Installation

0. Install the prerequisites above
1. Open a terminal and move to the directory in which you what to install the program. Skip this step (and ignore `<DIRECTORY>/` from now on) if the home folder is adequate for you.
``` sh
cd <DIRECTORY>
```
2. Clone the repository and move inside of it
``` sh
git clone https://github.com/albertcanales/reading-timeline.git && cd reading-timeline
```
3. Create the virtual environment with venv
``` sh
python3 -m venv env
```
4. Install required Python packages with pip
``` sh
env/bin/pip install -r requirements.txt
```

## Usage

To use the program, first move into the installation directory:
``` sh
cd <DIRECTORY>/reading-timeline
```

And run the program:
``` sh
env/bin/python main.py -vv
```

## Updating

To update to the latest features, first move into the installation directory:
``` sh
cd <DIRECTORY>/reading-timeline
```

And then pull the changes from master:
``` sh
git pull
```

## Contributing

Giving bug reports and feature requests is greatly appreciated. The easiest ways to do so are to [contact me directly](mailto:albertcanalesros@gmail.com) or to open an issue. You can also make a pull request, but I would recommend first getting in touch to ease the task of merging.

## Help

The following command shows the program's help and options:

	python main.yml -h

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

This project has been completely based on the great design from [
Jeff Allen](https://jamaps.github.io).

Thanks also to [Abel Doñate](https://abeldonate.com) for the ideas, testing and feedback.
