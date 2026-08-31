import json
import random
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREATURES_JSON = os.path.join(SCRIPT_DIR, "Creatures.JSON")

FLEE_CHANCE = 20/100
FLEE_SFX_DIR = "insert directory here!!!"

#chance creature flees
hasFled = random.random() < (FLEE_CHANCE)
if hasFled:
    print(["Oh. it fled. sorry...", FLEE_SFX_DIR])
    sys.exit()

#Special "shiny message" based on conditional probability
isShiny = random.random() < ((1 - FLEE_CHANCE) * 1/4096)

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
    
print([message, sfx])