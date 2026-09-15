import json
import random
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREATURES_JSON = os.path.join(SCRIPT_DIR, "Creatures.JSON")

SFX_DIR = os.path.join(SCRIPT_DIR, "SFX")

RESULT_FILE = os.path.join(SCRIPT_DIR, "HuntResult.txt")

FLEE_CHANCE = 20/100
FLEE_SFX = os.path.join(SFX_DIR, "flee.mp3")

TRAP_CHANCE = 20/100
TRAP_SFX = os.path.join(SFX_DIR, "trap.mp3")

def writeResult(message, sfx="", name=""):
    #line1 = msg, line2 = sfx path, blank if not exists.
    #See README.MD for more details on overall MixItUp integration.
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(f"{message}\n{sfx}\n{name}\n")

#chance creature flees
hasFled = random.random() < (FLEE_CHANCE)
if hasFled:
    writeResult("Oh. It fled. Sorry...", FLEE_SFX, "Fled")
    sys.exit()

hasTrapped = random.random() < (TRAP_CHANCE)
if hasTrapped:
    writeResult("Caught in a trap", TRAP_SFX, "Trap!")
    sys.exit()

#Special "shiny message" based on conditional probability
isShiny = random.random() < (1/4096)

#locate + open JSON data file in read
with open(CREATURES_JSON, "r", encoding="utf-8") as file:
    data = json.load(file)

#select random creature from JSON (in O(1); dictionary)
creatureName = random.choice(list(data.keys()))
chosen = data[creatureName]

defaultMessage = f"You have caught {creatureName}"
defaultSFX = ""

#output respective message for chosen creature
if isShiny:
    message = chosen.get(
        "shinyMessage",
        chosen.get("message", defaultMessage)
    )
    sfx = chosen.get(
        "shinyMessageSFX",
        chosen.get("messageSFX", defaultSFX)
    )
else:
    message = chosen.get("message", defaultMessage)
    sfx = chosen.get("messageSFX", defaultSFX)
    
writeResult(message, sfx, creatureName)
