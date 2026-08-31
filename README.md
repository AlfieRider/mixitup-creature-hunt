# Creature Hunt & Creature Manager
This repository includes a two-part tool for running a "Hunt for Creatures"-style Twitch channel point redeem. Inside are two executable files: CreatureHunt.py, which will be linked to the redeem in MixItUp (further detail provided later), and CreatureManager.py, a friendly GUI to ensure that managing the creature pool is as accessible as possible.

## Files
Provided below is a table which describes each file in this repository, and breadth on how to use it.
| File Name | Intended Purpose |
|-----------|------------------|
| CreatureManager.py | GUI app for adding, editing, renaming, and deleting creatures. Used ideally outside of stream. |
| CreatureHunt.py | The script which MixItUp runs on redeem. Picks a random creature, rolls flee/shiny odds, and outputs the result|
| Creatures.JSON | The data file both scripts read to and/or write from. Created automatically the first time a creature is saved in the manager |
| HuntResult.txt | Written fresh by CreatureHunt.py on every redeem; line 1 is the chat message, line 2 is the SFX path (blank if none). MixItUp reads from this, rather than the program output. |
| SFX/ | Folder for relevant sound files associated with the redeem. CreatureHunt.py expects a flee.mp3 for the flee outcome (provided and changeable); individual creature SFX are chosen freely via the Creature Manager file picker, and may live anywhere on the disk |

## Requirements
- Python 3.8/newer
- tkinter - included with most python installs by default. If the Manager fails to launch with a `ModuleNotFoudnError: No module named 'tkinter'`, then this should be installed separately. Windows/MAC has it bundled with Python, whilst Linux users should `sudo apt install python3-tk`.
- No other 3rd party packages required, as all other libraries are included in Python's standard library. For documentation sake, they are listed as follows: json, random, sys, os, re, (tkinter).

## First-time Setup
1. Ensure that `CreatureManager.py` and `CreatureHunt.py` are in the same folder.
2. Run CreatureManager.py and add at least one creature before going live (see the "+" on the Left Hand Side).
3. Ensure this creature has been added AND saved, as if the redeem is fired before this entry is made, then a `File-not-found error` will occur. Adding a creature through the manager creates the file automatically, so ensure that this occurs before a user can redeem the respective redeem. 
4. Confirm the two scripts are pointed at the same `Creatures.JSON` - both currently expect it in the same folder of which they are ran from. This is resolved relative to the scripts' own location (not wherever they're launched from), so it works whether double-clicked to run or run from a terminal/IDE.
5. A flee sound effect, if wished for, should be named exactly `flee.mp3` inside an SFX folder next to the scripts. This path is currently hardcoded. A flee.mp3 is already provided! So only do this if you'd like a unique one.

## Using Creature Manager
- Adding a creature: click "+" in the top-left. New entries are auto-named "new-creature1", "new-creature2", ..., "new-creature(n)" for n new entries. This is to avoid collisions.
- Editing a creature: click on the creature's name in the given list (see the left of the screen), and you will be shown the current contents of this creature entry on the right of the screen. You can edit not only the Message and ShinyMessage boxes, but also the creature's name itself.
- Message vs ShinyMessage: Message will be outputted upon a normal result from `CreatureHunt.py`. ShinyMessage will be outputted for a creature if the shiny check has succeeded in `CreatureHunt.py`. By default, if no message or shiny message is defined, the default "You have caught _CreatureName_" will be outputted.
- MessageSFX / ShinyMessageSFX: an optional sound file path for each outcome. Either type the file path in the input box, or click the `[>] File Input` button beneath either field to navigate via file explorer instead (which filters for valid audio files). The path will then be automatically filled after selection. When manually typing the path, please ensure it is correct, as their is currently no validation for this!!!
- Renaming: click 'Rename' next to the creature's name. Only letters (both cases), numbers, "_", and "-" are permitted. Duplicate names are also blocked.
- Deleting: the red 'Delete Creature' button asks for delete confirmation, then will show a 5 second countdown before the window closes (upon confirming).
- Switching creatures with unsaved edits: this application will always ask before discarding unsaved changes, whether due to clicking a different creature, closing the application, or reloading the JSON (in case of external editing).
- Settings ('⚙', in the top right):
    - Toggle Dark Mode: visual change only, with no effect on data.
    - Reload from JSON: re-reads `Creatures.JSON` and refreshes the application. Useful if the file was edited manually outside of the app. Warns first if you have unsaved edits.

## How CreatureHunt.py works
Each time a twitch-user hits the redeem in chat, MixItUp will run CreatureHunt.py, which does the following:
1. Flee Check: currently, the code dictates a 20% chance that the creature will flee. On flee, the script outputs a flee message alongside the `SFX/flee.mp3` path, exiting immediately (i.e. no creature or shiny roll occurs on flee).
2. Shiny check: rolled post-flee check, independent of which creature ends up being chosen.
3. Creature selection: a random creature is selected from every entry in Creatures.JSON, each equally likely `P(chosen)=1/n`.
4. Output: builds a pair of outputs, consisting of the Message and SFX path. Using ShinyMessage\SFX if the shiny check succeeded (and if either are defined), falling back of regular message/sfx, and falling back further to a default "You have caught {name}" with no SFX path defined for said creature. This is then written to HuntResult.txt as two lines (message \n SFX path) rather than outputted to the console. The below explains this further.

## How shiny odds work.
This section is currently pending; the exact numbers for ensuring a 1/4096 probability are being adjusted and finalised.

## Why the output goes to a .txt file, and not the console:
Earlier versions of `CreatureHunt.py` used `print([message, sfx])` and other similar formats. However, MixItUp External Program action has no way to parse this kind of listed output into two separate values, and doesn't support array-style indexing, or even a string-splitting function in its actions set, thus this original formatting couldn't be reconciled on MixItUp's end.

To resolve this, `CreatureHunt.py` now writes to `HuntResult.txt`, following the convention shown below:
```
line1: the chat message
line2: the sfx path (or a blank line if this doesn't exist)
```

## How to Link to MixItUp:
1. Enter the usual MixItUp system.
2. In Channel Point Rewards (or Commands), create and name the redeem to your pleasing.
3. Under the Actions list, click '+' and select 'External Program'.
4. Set the `Program File Path` to your actual `python.exe` (no the `.py` script). This is because MixItUp doesn't shell-execute by default, thus requires the real executable here. Use methods such as `where python` or searching for `python.exe` to locate this.
5. Set the `Program Arguments` to the full path of `CreatureHunt.py` (e.g: `"C:\Folder\CreatureHunt.py"`)
6. Toggle `Wait Until Complete` ON, ensuring the file exists by the time the action runs. `Save Output` is counterintuitively not required, as the output we desire is from `HuntResult.txt`.
7. Add a `File Action`, set to `Read Specific Line From File`. The `file path` is to `CreatureHunt.py`, line number 1 should be saved to a Special Identifier, e.g. `$huntMessage`.
8. Add a second `File Action` pathed to the same `CreatureHunt.py`. Set line number 2 to be saved to a different identifier, such as `$huntSFX`.
9. Add a `Chat action`, and use `$huntMessage` in the text as required.
10. Add a `Conditional Action`, such that if `$huntSFX` is not equal (`!=`) to an empty value (`""`), run a `Sound Action` using `$huntSFX` as the file path.

## ⚠️ MUST DO's before going live
Please confirm that:
1. The creature pool has not been set to zero. This can be viewed in the CreatureManager. At least one entry at a time must be ensured.
2. The two `File Actions` in MixItUp point at the correct, exact `HuntResult.txt` path. This must match the `SCRIPT_DIR` from `CreatureHunt.py`, i.e. wherever this script actually lives.
3. MixItUp wiring is otherwise fully complete as written above, and has been tested with a real redeem before going live.

## Known limitations
- No confirmation prompt if JSON pool is manually edited (i.e outside the manager). Malformed entries are silently be skipped over by .get() fallbacks rather than causing an error, so a typo'd error will simply raise a visible warning. To avoid this, only edit the JSON through the manager ideally. One or the other at a time, not both.
- `CreatureManager.py` and `CreatureHunt.py` don't coordinate file access. In other words, there is a window where, if editing the creature pool live, the user could redeem against a half-written entry. Concurrent access and Isolation (from ACID) will be implemented later on. Please bare with.
- A manually-typed audio file path currently has zero validation on save. The file explorer input feature itself does this, however the input boxes themselves don't check for things such as correct file extension, valid path format, etc.
- `HuntResult.py` is overwritten with every redeem. This could potentially cause issues if two users could redeem this simultaneously. A "per-viewer" system could be implemented, but for now, a cooldown on this redeem (even 30 seconds) would completely prevent this.
- Fleeing probability and shiny probability are likely incorrect, as FLEE_CHANCE is factored in twice. As mentioned above, this Shiny Probability needs to be adjusted and finalised.

## Extra information - Project origins
A Twitch Streamer reached out to me regarding their existing twitch redeem, being Mesian Velari's "Shiny Wooper Hunt". The original text file and endless lines of `elif` selection statements with O(n) access also was asking for a little upgrade, for lack of better phrasing. Thus the `O(1) solution` was very quickly born. CreatureManager.py only came to exist as I thought I'd save Mesian from having to learn JSON. Ever since, through remote tinkering with MixItUp (and a few late-evening...'requirement gathering' calls), this has finally been fully integrated into their Twitch Viewer Redeem engagement system. This has now been proved to incredibly simplify the process, management and setup of the redeem and it's inner workings. Thank you Mesian Velari for this incredibly fun mini-project! Those interested in seeing this in-action (minus the setup; as a "reedemer") are invited to check Mesian Velari's stream page on twitch.


