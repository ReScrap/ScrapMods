# Scrapland Mods

This repository is a just my playground where I learn how to mod Scrapland and
try to make something useful and/or fun. Don't take this repository too serous.
It is no near good example on modding Scrapland. I am just playing around here 😅.

**Warning**: everything in here is **in development**! \
Anything, at any time can stop work properly, crash your game, set your pc on
fire, start cancer or kill your dog. Use it on your own.

## Table of content

* [Requirements](#requirements)
* [build.ps1](#buildps1)
    * [Setup](#setup)
	* [How to use](#how-to-use)
* [Mods structure](#mods-structure)
    * [Simple mod](#simple-mod)
    * [Mod with misc](#mod-with-misc)
* [Existing mods](#existing-mods)
* [Useful links](#useful-links)

## Requirements

For building `.packed` files with `build.sh` I use [ScrapPackedExplorer](https://github.com/romibi/Scrap-Packed-Explorer).
If you want to use my `build.sh`  you need to use ScrapPackedExplorer >= 0.3.1.

For compiling `.py` to `.pyc` you need [Python 1.5.2](https://www.python.org/download/releases/1.5/).

And preferably you need to have any version of Scrapland itself 😄.

## build.ps1

`build.ps1` is a script that can build, install and uninstall mods from this
repo.

### Setup

To use `build.ps1` you need to do 2 simple steps:

  1. Copy `config.example.ps1` to `config.ps1`
  2. Change paths to `ScrapPackedExplorer`, `Python 1.5.2` and `Scrapland` to yours.

```powershell
$packed_explorer_path = '..\bins\spe.exe';
$pyhton_path          = 'C:\Program Files (x86)\Python\python.exe';
$scrapland_path       = 'D:\Games\SteamLibrary\steamapps\common\Scrapland';
```

If you will not do this 2 steps `build.ps1` will use default variables.

### How to use it

Building mods:

```powershell
.\build.ps1          # If no argument specified will build all folders except 'bin' and 'out'
.\build.ps1 ModName  # Will build mod from folder "ModName"
```

Flags:

```powershell
.\build.ps1 -i --install   # Installs mod after building it
.\build.ps1 -u --uninstall # Instead of building mod will uninstall it
```

Mods will be in the `out` folder

Every folder is a separate mod.

## Mods structure

There is 2 types of "configuration" of mod folder: *simple* and *with misc*

### Simple mod

Everything in mod folder except `README.md` will be packed in `.packed` file. That's it. Pretty
simple.

### Mod with misc

```
..
ModFolder\
|__ packed\
|____ ...
|__ misc\
|____ ...
```

Everything in `packed` folder will be packed in `.packed` file.
Everything in `misc` folder will be copied to the game folder. If that file is
already exists, original file will be backed-up and re-installed on its place on
uninstalling mod.


## Existing mods:

 - Loader: Contains just `scripts/init.py`.
 - Logger: Contains... logger. How surprising.
 - Police2Gear: Replaces default money-bagging police action to transforming to armed police
 - ScorerPlayground: Just playground for working with `SScorer` where I try to make custom menus

Check out `ModName/README.md` for more info.

## Useful links

 - [Python 1.5.2](https://www.python.org/download/releases/1.5/)
 - [ScrapPackedExplorer](https://github.com/romibi/Scrap-Packed-Explorer) (@romibi)
 - [ScrapHacks](https://gitdab.com/SREP/ScrapHacks) - tools and documenation for reverse-engeenering Scrapland (@earthnuker)
 - [Notes about how game engine works](https://gitdab.com/SREP/Notes) (@earthnuker)
 - [My mods loader for Scrapland](https://gitdab.com/SREP/ScrapModLoader). Depricated, will work on this sometimes later when I learn more about modding Scrapland
 - [Scrapland Discord server](https://discord.gg/eBw2Pzpu4w)
