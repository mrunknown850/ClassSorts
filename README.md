# ClassSorts
If your classroom's seats are constantly changing in a specific pattern, this program will automatically generate a classroom diagram. Use the guide below for settings and [how to use](#1-how-to-use).

## 1. How to use?
* Download the entire source code because I can't make executable lol.
* Run the __main.py__ file located in the project's root directory.
* Choose either [*Cycle Mode*](#3-what-is-the-cycle-mode) or [*Initialize Mode*](#2-what-is-the-initialize-mode).
* Confirm the datas and press *Enter* to execute.
* After either using the Initialize Mode or Cycle Mode, the script will generate an `output.html` file. Open the file in your browser and use the built-in print function to print out the classroom's diagram.

## 2. What is the *Initialize Mode?*
For first time user, using *Initialize Mode* is forced. **Initialize Mode** will generate a reusable version of the input diagram for the program to use again when got executed again. This features is use when you are the *first time user*, *class layout changed completely* or *missing diagram for the programs*.
* First, setup the initial layout in `\input\input_layout.txt` file. Here is an example of the input file format.
```
Human 1.1 | Human 1.2
Human 1.3 | Human 1.4

Human 2.1 | Human 2.2
Human 2.3 | Human 2.4

Human 3.1 | Human 3.2
Human 3.3 | Human 3.4

Human 4.1 | Human 4.2
Human 4.3 | Human 4.4
```
![The output of the example shown above](/example.png)
Each non-empty line is defining a set of 2 people that sit next to eachother within a table, seperated by a seperation character that can be changed in the [configuration file](#4-settings-configurations). In this case the *seperation charactor* is "` | `". Each row of the people are seperated by an empty line as shown above. The "Entrace" and "Teacher's Table" name can be changed in the configuration file as well.
* After that change some settings in the **\input\settings.json** file. Follow [this guide](#4-settings-configurations) for settings.
* And finally when execute `main.py`, choose `I` for Initialize Mode.
* Verify the `Initialize Week` and press `Enter` to continue.

## 3. What is the *Cycle Mode?*
Use **Cycle Mode** when you already got the reusable version of the input diagram and want to generate a new diagram of the next week following the pattern defined in the [configuration file](#4-settings-configurations).
* Just execute the `main.py` file and choose `C` for Cycle Mode.
* Verify the `current` and `generating week` then press `Enter` to continue.

## 4. Settings configurations
To change most of the settings of the program, please follow the table below.
| Settings Name | Type | Usage | Default |
|---------------|------|-------|---------|
|`currentWeekNo`|`int`|Configure the starting week when using [initialize mode](#2-what-is-the-initialize-mode).|1|
|`rowShiftCycle`|`int`|How much table does all table is pushed backward|1|
|`groupShiftCycle`|`int`|How much row does all row get is offset to the right|1|
|`rowShiftDuration`|`int`|How many week does it take to do 1 row shifting cycle|1|
|`groupShiftDuration`|`int`|How many week does it take to do 1 group shifting cycle|2|
|`rowDurationOffset`|`bool`|Offset the rowShiftDuration by 1. Example: Move every 2 weeks but only only on odd weeks|true|
|`groupDurationOffset`|`bool`|Offset the groupShiftDuration by 1. Similar to `rowDurationOffset`|true|
|`seperationChar`|`str`|The seperating character. Only used in [initialize mode](#2-what-is-the-initialize-mode).|`" \| "`|
|`classEntranceTitle`|`str`|The title of the `classEntrance` block.|`"Entrance"`|
|`teachersTableTitle`|`str`|The title of the `teachersTable` block.|`"Teacher's Table"`|

