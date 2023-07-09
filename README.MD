[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# Inventory Salvage
> Like the project? Leave a star, it helps! ;)

**Release 0.1.0**

## Description
This is an app that allows you to salvage information from a lost minecraft account.

Minecraft servers (and personal worlds) store player files using the uuid of the player account. This file contains all of the inventory, ender chest, position, advancements, recipes, etc., and the purpose of this app is to make it easy to copy from an old player file onto a new player file all of the desired data. This is not for duping.

It's mostly useless but I wanted to code this weekend.


## Installation
### Get the app!
- There is a new release v0.1.0 in [releases](https://github.com/Heat-GradientAscent/inventory-salvage/releases)

## Contribute
### Requirements
- Have Python 3.10.7+ installed in your system
- Have pip3 installed
- Know how to python and git

### Setup
- Clone repository
- Navigate to root dir, then run commands
  - `python -m venv .\venv`
  - `.\venv\scripts\activate`
  - `python -m pip install -r requirements.txt`
  - Don't forget to set your python version to the virtual environment (venv)

### Introduce new packages used
- Navigate to root dir, then run command
  - `python -m pip freeze > requirements.txt`

### Build
- Navigate to root dir, then run command (command can be found in build.txt)
  - `pyinstaller --noconfirm --onefile --windowed --icon "src/assets/fave.ico" --name "inventory-salvage" --clean --paths "src/assets/*.ico" --add-data "src/assets/fave.ico;assets" --exclude-module iconpath "src/main.py"`

### Run
- Navigate to `main.py` and run the file normally

### Open a pull request (I doubt anyone will)
- Once you've finished adding changes, add yourself as a contributor below
- Open your pull request, and @ [me](https://github.com/Heat-GradientAscent)


## Contributors
- [Your name](https://github.com)


## License
Licensed under the [GNU GPL v3 license](LICENSE).
