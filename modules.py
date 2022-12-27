import random, discord
allowedIDs = [284479093443919872,792432422071173131]
def idVerify(id):
    return id in allowedIDs
#botResponses = ["dev server gaming"]
botResponses = ["Are flying squirrels real? Scientists don't think so anymore now with this breath-taking information..","are you stupid or are you stupid","holy smokes!","I LOVE MARKERS","Join Unitology. We have cheesecakes.","man i could kill for a steak right now","you suck","man im tired of seeing you do loser things like a big loser","awesome sauce","that's too bad","why would he do this","oh yes! our table! its fixed!","ds13 catgirls confirmed","i REALLY love catgirls","you have such a loser mindset","what? chinese elon musk???"]
def botFooter():
    return random.choice(botResponses)
def cembed(ctx,title,description,color=discord.Color.random()):
    embed = discord.Embed(title=title,description=description,color=color)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.set_footer(text=botFooter(),icon_url="https://cdn.discordapp.com/avatars/1010706026112241776/1796c013a1e72e35e35dae51f3029f11.webp?size=1024")
    return embed #I am retarded. How did I forget to add this for so fucking long???
async def user_input(bot,user, message):
	answer = await bot.wait_for("message", check=lambda response: response.author == user and response.channel == message.channel)
	answer = answer.content
	answer = answer.lower().strip()

	return answer
def stringifyList(list):
    return '\n'.join(list)
def stringifyListThruKey(list,key):
    s = ''
    for dic in list:
        #print(dic[key])
        s += dic[key] + "\n"
    #print(s)
    return s

gameTemp = {
    '_id': 1,
    'turn': 0,
    'defcon': 5
}

validContinents = ['Africa', 'Asia', 'Oceania', 'Europe', 'North America', 'South America']

resources = {
    "iron": {
        "required_tech": None,
        "name": "Iron"
    },
    "tungsten": {
        "required_tech": None,
        "name": "Tungsten"
    },
    "silver": {
        "required_tech": "silver quarries",
        "name": "Silver"
    },
    "electronics": {
        "required_tech": None,
        "name": "Simple Electronics"
    },
    "deeznutsium": {
        "required_tech": "devmode",
        "name": "Deeznutsium"
    },
    "steel": {
        "required_tech": "steel processing",
        "name": "Steel"
    },
    "cryo-trillium": {
        "required_tech": "biomatter cryogenics",
        "name": "Cryo-Trillium"
    },
    "phytonium": {
        "required_tech": "biomatter packing",
        "name": "Phytonium"
    }
}

buildings = {
    "small iron quarry": {
        "name": "Small Iron Quarry",
        "cost": {
            "population": 10,
            "tungsten": 10,
            "electronics": 5,
            "energy": 5
        },
        "production": {
            "iron": 15,
            "energy": -2
        },
        "tech": [],
        "hp": 100,
        "type": "production"
    },
    "small solar grid": {
        "name": "Small Solar Grid",
        "cost": {
            "iron": 20,
            "electronics": 10,
            "population": 5
        },
        "production": {
            "energy": 10,
            "iron": -5
        },
        "tech": [],
        "hp": 100,
        "type": "production"
    },
    "small apartment": {
        "name": "Small Apartment Building",
        "cost": {
            "iron": 15,
            "tungsten": 5
        },
        "production": {
            "energy": -5,
            "food": -5,
            "population": 5
        },
        "tech": [],
        "hp": 50,
        "type": "production"
    },
    "small farm": {
        "name": "Small Farming Plot",
        "cost": {
            "population": 5,
            "iron": 10,
            "energy": 2
        },
        "production": {
            "energy": -5,
            "food": 10
        },
        "tech": [],
        "hp": 25,
        "type": "production"
    },
    "local research lab": {
        "name": "Local Research Lab",
        "cost": {
            "iron": 50,
            "electronics": 25,
            "population": 10
        },
        "sci_points": {
            "PHYSICS": 10,
            "ENGINEERING": 5,
            "THERMODYNAMICS": 5
        },
        "tech": ["basic physics"],
        "hp": 75,
        "type": "tech_production"
    },
    "cryogenic processing facility": {
        "name": "Cryogenic Processing Facility",
        "cost": {
            "iron": 75,
            "steel": 25,
            "electronics": 15,
            "population": 15,
            "energy": 10
        },
        "production": {
            "energy": -15,
            "steel": -10,
            "iron": -10,
            "cryo-trillium": 10
        },
        "tech": ["biomatter cryogenics"],
        "hp": 250,
        "type": "production"
    },
    "steel alloying plant": {
        "name": "Steel Alloy Plant",
        "cost": {
            "iron": 30,
            "electronics": 5,
            "energy": 5,
            "population": 5
        },
        "production": {
            "energy": -5,
            "iron": -10,
            "steel": 10
        },
        "tech": ["steel processing"],
        "hp": 125,
        "type": "production"
    },
    "basic silver quarry": {
        "name": "Basic Silver Quarry",
        "cost": {
            "iron": 20,
            "tungsten": 5,
            "energy": 5,
            "population": 5
        },
        "production": {
            "silver": 5,
            "energy": -5
        },
        "tech": ["silver quarries"],
        "hp": 100,
        "type": "production"
    },
    "basic electronic manufactory": {
        "name": "Basic Electronic Manufactory",
        "cost": {
            "steel": 15,
            "iron": 10,
            "tungsten": 5,
            "energy": 10,
            "population": 10
        },
        "production": {
            "electronics": 15,
            "iron": -10,
            "silver": -10,
            "energy": -10
        },
        "tech": ["steel processing", "electronic processing"],
        "hp": 150,
        "type": "production"
    }
}

technologies = {
    "silver quarries": {
        "name": "Silver Extraction",
        "sci_points": {
            "ENGINEERING": 15
        },
        "requires": ["basic physics"]
    },
    "steel processing": {
        "name": "Steel Processing",
        "sci_points": {
            "PHYSICS": 5,
            "ENGINEERING": 20
        },
        "requires": ["basic physics"]
    },
    "electronic processing": {
        "name": "Basic Electronic Processing",
        "sci_points": {
            "PHYSICS": 10,
            "ENGINEERING": 15
        },
        "requires": ["basic physics", "silver quarries", "steel processing"]
    },
    "basic physics": {
        "name": "Idea of Physics",
        "sci_points": {
            "PHYSICS": 15
        },
        "requires": []
    },
    "phytonium packing": {
        "name": "Phytonium Collection & Packaging",
        "sci_points": {
            "PHYSICS": 10,
            "ENGINEERING": 25
        },
        "requires": ["basic physics"]
    },
    "biomatter cryogenics": {
        "name": "Biomatter Cryogenics",
        "sci_points": {
            "THERMODYNAMICS": 25,
            "PHYSICS": 50,
            "ENGINEERING": 10
        },
        "requires": ["basic physics", "steel processing", "phytonium packing"]
    },
    "devmode": {
        "sci_points": {
            "quaternions": 1
        },
        "requires": ["admin"]
    }
}

techTypes = {
    "PHYSICS": "Physics",
    "ENGINEERING": "Mechanical Engineering",
    "THERMODYNAMICS": "Thermodynamics",
    "AERODYNAMICS": "Aerodynamics",
    "QUANTUM_PHYSICS": "Quantum Mechanics",
    "CHEMISTRY": "Chemistry"
}

techInProgress = {
    "PHYSICS": 0,
    "ENGINEERING": 0,
    "THERMODYNAMICS": 0,
    "AERODYNAMICS": 0,
    "QUANTUM_PHYSICS": 0,
    "CHEMISTRY": 0
}

districtTemplate = {
    "name": "",
    "originalOwner": "",
    "owner": "",
    "capacity": 5,
    "buildings": []
}

nationData = {
    "_id": None,
    "channelid": None,
    "name": None,
    "type": "nation",
    "location": None,
    "tech_complete": [],
    "tech_progression": {},
    "resources": {
        "iron": 100,
        "tungsten": 50,
        "silver": 0,
        "electronics": 60,
        "energy": 25,
        "population": 25,
        "deeznutsium": 0,
        "phytonium": 0,
        "cryo-trillium": 0,
        "food": 150
    },
    #"buildings": [buildings.get("small iron quarry"),buildings.get("small solar grid")],
    "districts":[
        
    ],
    "warWith": [],#nation combat
    "conflictWith": [],#organization combat
    "trades":[

    ]
}