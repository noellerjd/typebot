
races = {
    "Dwarf": {
      "description": "Dwarf Desc",
      "traits": {
        "Speed": f'{25}, *your speed is not reduced by wearing heavy armor*',
        "Languages": ["Common", "Dwarvish"],
        "Abilities": "x",
        "subrace": {
            "Hill dwarf": {
                "ability increase": "Wisdom +1, Constitution +2",
                "race increase": "*Dwarven Toughness*: +1 Max Hit Point, Increases by 1 everytime you gain a level."
            },
            "Mountain dwarf": {
                "ability increase": "Strength +2, Constitution +2",
                "race increase": "*Dwarven Armor Training*: You have proficiency with light and medium armor"
            }
        } 
      }
    },
    "Elf": {
      "description": "Elf Desc",
      "traits": {
        "speed": 25,
        "languages": ["Common", "Brainrot"],
        "ability increase": "Constitution +69"
      }
    },
    "Donkey": {
      "description": "*Donkey Desc*",
      "traits": {
        "speed": 25,
        "languages": ["Common", "Brainrot"],
        "ability increase": "Constitution +69"
      }
    }
}
classes = {
  "Fighter": {
    "description": "A master of martial combat, skilled with a variety of weapons and armor.",
    "abilities": {
        "primary": "Strength",
        "secondary": "Constitution"
    }
    },
  "Wizard": {
    "description": "A scholarly magic-user capable of manipulating the structures of reality.",
    "abilities": {
        "primary": "Intelligence",
        "secondary": "Wisdom"
    }
  }
}

backgrounds = {
  "Soldier": {
    "description": "A warrior experienced in combat, having served in a military unit.",
    "skills": ["Athletics", "Intimidation"]
    },
  "Sage": {
    "description": "A learned individual devoted to the study of magic and ancient lore.",
    "skills": ["Arcana", "History"]
  }    
}