# Scrapland Mods

This repository is a just mine playground where I learn how to mod Scrapland and
try to make something useful and/or fun. Don't take this repository too serous.
It is no near good example on moding Scrapland. I am just plaing around here 😅.

## Requirements

For building `.packed` files in scripts I use [ScrapPackedExplorer](https://github.com/romibi/Scrap-Packed-Explorer).
If you want to use my scripts you need to use ScrapPackedExplorer >= 0.3.1.

For compiling `.py` to `.pyc` you need [Python 1.5.2](https://www.python.org/download/releases/1.5/).

And preferably you need to have any verison of Scrapland itself 😄.

## build.ps1

`build.ps1` is a script that can build, insatll and uninstall mods fromt this
repo.

### Setup

To use `build.ps1` you need specify 3 varables at the top of the script: path to
ScrapPackedExplorer, Python 1.5.2 and Scrapland:

```powershell
$pack_expl_path = '..\bins\spe.exe';
$pyhton_path    = 'C:\Program Files (x86)\Python\python.exe';
$scrapland_path = 'D:\Games\SteamLibrary\steamapps\common\Scrapland';
```

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

Everyting in mod folder except `README.md` will be packed in `.packed` file. That's it. Pretty
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

Everyting in `packed` folder will be packed in `.packed` file.
Everyting in `misc` folder will be copied to the game folder. If that file is
aredy exists, original file will be backed-up and re-installed on its place on
uninstalling mod.
