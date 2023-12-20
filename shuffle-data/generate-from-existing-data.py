from data_handlers import pokemon_data, move_data, item_data
import yaml

pokeDataFiles = {
    "constants"             : '../constants/pokemon_constants.asm',
    "names"                 : '../data/pokemon/names.asm',
    "baseStats"             : '../data/pokemon/base_stats.asm',
    "evosAttacksKanto"      : '../data/pokemon/evos_attacks_kanto.asm',
    "evosAttacksJohto"      : '../data/pokemon/evos_attacks_johto.asm',
    "eggMovesKanto"         : "../data/pokemon/egg_moves_kanto.asm",
    "eggMovesJohto"         : "../data/pokemon/egg_moves_johto.asm",
    "iconPointers"          : "../data/pokemon/icon_pointers.asm",
    "menuIcons"             : "../data/pokemon/menu_icons.asm",
    "menuIconPals"          : "../data/pokemon/menu_icon_pals.asm",
    "dexEntryPointers"      : "../data/pokemon/dex_entry_pointers.asm",
    "dexEntries"            : "../data/pokemon/dex_entries.asm",
    "dexOrderNew"           : "../data/pokemon/dex_order_new.asm",
    "dexOrderAlpha"         : "../data/pokemon/dex_order_alpha.asm",
    "picPointers"           : "../data/pokemon/pic_pointers.asm",
    "pokePalettes"          : "../data/pokemon/palettes.asm",
    "animPointers"          : "../gfx/pokemon/anim_pointers.asm",
    "anims"                 : "../gfx/pokemon/anims.asm",
    "idlePointers"          : "../gfx/pokemon/idle_pointers.asm",
    "idles"                 : "../gfx/pokemon/idles.asm",
    "pics"                  : "../gfx/pics.asm",
}

moveDataFiles = {
    "constants"             : '../constants/move_constants.asm',
    "names"                 : '../data/moves/names.asm',
    "characteristics"       : '../data/moves/moves.asm',
    "descriptionPointers"   : '../data/moves/descriptions.asm',
    "descriptions"          : '../data/moves/descriptions.asm',
    "animations"            : '../data/moves/animations.asm',
    "effectConstants"       : '../constants/move_effect_constants.asm',
}

itemDataFiles = {
    "constants"             : '../constants/item_constants.asm',
    "names"                 : '../data/items/names.asm',
    "descriptionPointers"   : '../data/items/descriptions.asm',
    "descriptions"          : '../data/items/descriptions.asm',
    "attributes"            : '../data/items/attributes.asm',
    "effects"               : '../engine/items/item_effects.asm',
    "apricornBalls"         : '../data/items/apricorn_balls.asm',
    "catchRateItems"        : '../data/items/catch_rate_items.asm',
    "healHP"                : '../data/items/heal_hp.asm',
    "healStatus"            : '../data/items/heal_status.asm',
    "mailItems"             : '../data/items/mail_items.asm',
}

baseStatFileBaseStatOrder = [
    "HP",
    "ATK",
    "DEF",
    "SPD",
    "SAT",
    "SDF"
]

evoMethodDataOrder = {
    "EVOLVE_LEVEL"      : ["Level", "Species"],
    "EVOLVE_ITEM"       : ["Used Item", "Species"],
    "EVOLVE_TRADE"      : ["Held Item", "Species"],
    "EVOLVE_HAPPINESS"  : ["Time", "Species"],
    "EVOLVE_STAT"       : ["Level", "Stat Relationship", "Species"]
}

dimensionsTranslation = {
    "U": 40,
    "f": 48,
    "w": 56,
}

# mapDataFiles {
#   "mapConstants": "../constants/map_constants.asm",

# }

# class pokedexHTMLBuilder:
#   def __init__(self, itemData, moveData)


class ItemDataBuilder:
    def __init__(self):
        self.itemData = []
        self.tmData = []
        self.hmData = []
        self.itemAttributesOrder = [
            "Price", 
            "Held Effect", 
            "Parameter", 
            "Property", 
            "Pocket", 
            "Field Menu", 
            "Battle Menu"
        ]

    def buildItemData(self):
        self.getConstants()
        self.getNames()
        self.getAttributes()
        self.getDescriptionPointers()
        self.getDescriptions()
        self.getItemEffects()

    def getConstants(self):
        self.getItemConstants()
        self.getTMConstants()
        self.getHMConstants()

    def getItemConstants(self):
        with open(itemDataFiles["constants"], "r") as f:
            for line in f:
                if "DEF NUM_ITEMS" in line:
                    break
                if line[0] == ";":
                    continue
                if "const " in line:
                    item = line.split("const ")
                    item = item[1]
                    item = item.split(";")
                    item = item[0].strip()
                    curItem = {"Constant": item}
                    self.itemData.append(curItem)

    def getTMConstants(self):
        with open(itemDataFiles["constants"], "r") as f:
            for line in f:
                if "DEF NUM_TMS" in line:
                    break
                if line[0] == ";":
                    continue
                if "add_tm " in line:
                    tm = line.split("add_tm ")
                    tm = tm[1]
                    tm = tm.split(";")
                    tm = tm[0].strip()
                    curTM = {"Constant": tm}
                    self.tmData.append(curTM)

    def getHMConstants(self):
        with open(itemDataFiles["constants"], "r") as f:
            for line in f:
                if "DEF NUM_HMS" in line:
                    break
                if line[0] == ";":
                    continue
                if "add_hm " in line:
                    hm = line.split("add_hm ")
                    hm = hm[1]
                    hm = hm.split(";")
                    hm = hm[0].strip()
                    curHM = {"Constant": hm}
                    self.hmData.append(curHM)

    def getNames(self):
        self.getItemNames()
        self.getTMNames()
        self.getHMNames()

    def getItemNames(self):
        i = 1  # skip NO_ITEM
        with open(itemDataFiles["names"], "r") as f:
            for line in f:
                if "assert_list_length NUM_ITEMS" in line:
                    break
                if line[0] == ";":
                    continue
                if "li " in line:
                    name = line.split("li ")
                    name = name[1].strip()
                    name = name.replace('"', "")
                    self.itemData[i]["Name"] = name.split(";")[0].strip()
                    i += 1

    def getTMNames(self):
        i = 0
        tms = False
        with open(itemDataFiles["names"], "r") as f:
            for line in f:
                if "NUM_TMS" in line:
                    break
                elif line[0] == ";":
                    continue
                elif tms:
                    if "li " in line:
                        name = line.split("li ")
                        name = name[1].strip()
                        name = name.replace('"', "")
                        self.tmData[i]["Name"] = name
                        i += 1
                else:
                    if "assert_list_length NUM_ITEMS" in line:
                        tms = True

    def getHMNames(self):
        i = 0
        hms = False
        with open(itemDataFiles["names"], "r") as f:
            for line in f:
                if "NUM_HMS" in line:
                    break
                elif line[0] == ";":
                    continue
                elif hms:
                    if "li " in line:
                        name = line.split("li ")
                        name = name[1].strip()
                        name = name.replace('"', "")
                        self.hmData[i]["Name"] = name
                        i += 1
                else:
                    if "assert_list_length NUM_ITEMS + NUM_TMS" in line:
                        hms = True

    def getAttributes(self):
        self.getItemAttributes()
        self.getTMAttributes()
        self.getHMAttributes()

    def getItemAttributes(self):
        i = 1  # skip NO_ITEM
        items = False
        with open(itemDataFiles["attributes"], "r") as f:
            for line in f:
                if "assert_table_length NUM_ITEMS" in line:
                    break
                elif line[0] == ";":
                    continue
                elif items:
                    if "item_attribute " in line:
                        attributes = line.split("item_attribute ")
                        attributes = attributes[1].split(",")
                        for j, attr in enumerate(attributes):
                            attrName = self.itemAttributesOrder[j]
                            self.itemData[i][attrName] = attr.strip()
                        i += 1
                elif "ItemAttributes" in line:
                    items = True

    def getTMAttributes(self):
        i = 0
        tms = False
        with open(itemDataFiles["attributes"], "r") as f:
            for line in f:
                if "assert_table_length NUM_ITEMS + NUM_TMS" in line:
                    break
                elif line[0] == ";":
                    continue
                elif tms:
                    if "item_attribute " in line:
                        attributes = line.split("item_attribute ")
                        attributes = attributes[1].split(",")
                        for j, attr in enumerate(attributes):
                            attrName = self.itemAttributesOrder[j]
                            self.tmData[i][attrName] = attr.strip()
                        i += 1
                elif "assert_table_length NUM_ITEMS" in line:
                    tms = True

    def getHMAttributes(self):
        i = 0
        hms = False
        with open(itemDataFiles["attributes"], "r") as f:
            for line in f:
                if "assert_table_length NUM_ITEMS + NUM_TMS + NUM_HMS" in line:
                    break
                elif line[0] == ";":
                    continue
                elif hms:
                    if "item_attribute " in line:
                        attributes = line.split("item_attribute ")
                        attributes = attributes[1].split(",")
                        for j, attr in enumerate(attributes):
                            attrName = self.itemAttributesOrder[j]
                            self.hmData[i][attrName] = attr.strip()
                        i += 1
                elif "assert_table_length NUM_ITEMS + NUM_TMS" in line:
                    hms = True

    def getDescriptionPointers(self):
        with open(itemDataFiles["descriptionPointers"], "r") as f:
            i = 1  # skip NO_ITEM
            for line in f:
                if line[0] == ";":
                    continue
                if "assert_table_length NUM_ITEMS" in line:
                    break
                elif "dw " in line:
                    pointer = line.split("dw ")
                    pointer = pointer[1].strip()
                    self.itemData[i]["Description Pointer"] = pointer
                    i += 1

    def getDescriptions(self):
        descriptions = {}
        curPointers = []
        curDescription = ""
        with open(itemDataFiles["descriptions"], "r") as f:
            for line in f:
                if line[0] == ";":
                    continue
                elif "dw " in line:
                    continue
                # If a pointer...
                elif "Desc:" in line:
                    curPointers.append(line.strip().replace(":", ""))
                # If part of description
                elif '"' in line:
                    descrip = line.split('"')
                    descrip = descrip[1].strip()
                    # Check if it ends with a hypen
                    seperator = " "
                    if descrip[-1] == "-":
                        seperator = ""
                        descrip = descrip[0:len(descrip) - 1]
                    curDescription += seperator + descrip
                    # Check if end of Description
                    if descrip[-1] == '@':
                        for pointer in curPointers:
                            descriptions[pointer] = curDescription.replace("@", "").strip()
                        curPointers.clear()
                        curDescription = ""
        for i, item in enumerate(self.itemData):
            if "Description Pointer" in item:
                if item["Description Pointer"] in descriptions:
                    itemDescription = descriptions[item["Description Pointer"]]
                    self.itemData[i]["Description"] = itemDescription

    def getItemEffects(self):
        i = 1  # skip NO_ITEM
        with open(itemDataFiles["effects"], "r") as f:
            for line in f:
                if "assert_table_length NUM_ITEMS" in line:
                    break
                if "dw " in line:
                    effect = line.split("dw ")
                    effect = effect[1]
                    effect = effect.split(";")
                    effect = effect[0].strip()
                    self.itemData[i]["Effect"] = effect
                    i += 1


class MoveDataBuilder:
    def __init__(self):
        self.moveData = []

    def buildMoveData(self):
        self.getConstants()
        self.getNames()
        self.getAttributes()
        self.getDescriptionPointers()
        self.getDescriptions()
        self.getAnimations()

    def getConstants(self):
        with open(moveDataFiles["constants"], "r") as f:
            for line in f:
                if "DEF NUM_ATTACKS" in line:
                    break
                if line[0] == ";":
                    continue
                if "const " in line:
                    move = line.split("const")
                    move = move[1]
                    move = move.split(";")
                    move = move[0].strip()
                    curMove = {"Constant": move}
                    self.moveData.append(curMove)

    def getNames(self):
        with open(moveDataFiles["names"], "r") as f:
            i = 1 # Skip NO_MOVE
            for line in f:
                if "li " in line:
                    curMove = line.split("li")
                    curMove = curMove[1].replace('"', "").strip()
                    self.moveData[i]["Name"] = curMove
                    i += 1

    def getAttributes(self, attributes=False):
        # attributes = [
        #     "Animation",
        #     "Effect",
        #     "Power",
        #     "Type",
        #     "Accuracy",
        #     "PP",
        #     "Effect Chance"
        # ]
        attributes = [
            "Effect",
            "Power",
            "Type",
            "Category",
            "Accuracy",
            "PP",
            "Effect Chance"
        ]
        with open(moveDataFiles["characteristics"], "r") as f:
            ready = False
            i = 1 # Skip NO_MOVE
            for line in f:
                if ready:
                    if line[0] == ";":
                        continue
                    if "move" in line:
                        curMove = line.split("move")
                        curMove = curMove[1].split(",")
                        for j, attr in enumerate(curMove):
                            self.moveData[i][attributes[j]] = attr.split(";")[0].strip()
                        i += 1
                elif "Moves1:" in line:
                    ready = True

    def getDescriptionPointers(self):
        with open(moveDataFiles["descriptionPointers"], "r") as f:
            i = 1 # Skip NO_MOVE
            for line in f:
                if line[0] == ";":
                    continue
                if ".IndirectEnd" in line:
                    break
                elif "dw " in line:
                    pointer = line.split("dw ")
                    pointer = pointer[1].strip()
                    self.moveData[i]["Description Pointer"] = pointer
                    i += 1

    def getDescriptions(self):
        descriptions = {}
        curPointers = []
        curDescription = ""
        with open(moveDataFiles["descriptions"], "r") as f:
            for line in f:
                if line[0] == ";":
                    continue
                elif "dw " in line:
                    continue
                # If a pointer...
                elif "Description:" in line:
                    curPointers.append(line.strip().replace(":", ""))
                # If part of description
                elif '"' in line:
                    descrip = line.split('"')
                    descrip = descrip[1].strip()
                    # Check if it ends with a hypen
                    seperator = " "
                    if descrip[-1] == "-":
                        seperator = ""
                        descrip = descrip[0:len(descrip) - 1]
                    curDescription += seperator + descrip
                    # Check if end of Description
                    if descrip[-1] == '@':
                        for pointer in curPointers:
                            descriptions[pointer] = curDescription.replace("@", "").strip()
                        curPointers.clear()
                        curDescription = ""
        for i, move in enumerate(self.moveData):
            if "Description Pointer" in move:
                if move["Description Pointer"] in descriptions:
                    moveDescription = descriptions[move["Description Pointer"]]
                    self.moveData[i]["Description"] = moveDescription
    
    def getAnimations(self):
        with open(moveDataFiles["animations"], "r") as f:
            ready = False
            i = 0
            for line in f:
                if ready:
                    if line[0] == ";":
                        continue
                    if "dw" in line:
                        curAnim = line.split("dw")
                        curAnim = curAnim[1]
                        self.moveData[i]["Animation"] = curAnim.split(";")[0].strip()
                        i += 1
                    if "assert_table_length NUM_ATTACKS" in line:
                        ready = False
                elif "BattleAnimations" in line:
                    ready = True


class PokemonDataBuilder:
    def __init__(self):
        self.pokemonData = []

    def buildPokemonData(self):
        self.getConstants()
        self.getNames()
        self.getBaseStatsDataFiles()
        self.processBaseStatsDataFiles()
        self.getEvosAttacksPointers()
        self.getEvosAttacks()
        self.getEggMovePointers()
        self.getEggMoves()
        self.getMenuIcons()
        self.getMenuPals()
        self.getDexEntryPointers()
        self.getDexEntryFiles()
        self.processDexEntryFiles()
        self.getDexOrderNew()
        self.getDexOrderAlpha()
        self.getPicPointers()
        self.getPalettes()
        self.getPics()

    def getConstants(self):
        with open(pokeDataFiles["constants"], "r") as f:
            region = "KANTO"
            for line in f:
                # Add handling for unown later.
                if "DEF NUM_POKEMON EQU" in line:
                    break
                if "JOHTO_POKEMON" in line:
                    region = "JOHTO"
                if "const " in line:
                    curPoke = line.split("const")
                    curPoke = curPoke[1]
                    curPoke = curPoke.split(";")
                    curPoke = curPoke[0].strip()
                    curPoke = {
                        "Constant": curPoke,
                        "Region": region
                    }
                    self.pokemonData.append(curPoke)

    def getNames(self):
        ready = False
        with open(pokeDataFiles["names"], "r") as f:
            i = 0
            for line in f:
                if ready:
                    if "db" in line:
                        curPoke = line.split("db ")
                        curPoke = curPoke[1]
                        curPoke = curPoke.replace('"', "")
                        curPoke = curPoke.replace("@", "")
                        self.pokemonData[i]["Name"] = curPoke.strip()
                        i += 1
                elif "PokemonNames::" in line:
                    ready = True

    def getBaseStatsDataFiles(self):
        with open(pokeDataFiles["baseStats"], "r") as f:
            i = 0
            for line in f:
                if "INCLUDE" in line:
                    curStatFile = line.split("INCLUDE ")
                    curStatFile = curStatFile[1]
                    curStatFile = curStatFile.split('"')
                    curStatFile = curStatFile[1]
                    curStatFile = "../" + curStatFile
                    self.pokemonData[i]["BaseStatFile"] = curStatFile
                    i += 1

    def processBaseStatsDataFiles(self):
        for i, poke in enumerate(self.pokemonData):
            with open(poke["BaseStatFile"], "r") as f:
                j = 0
                for line in f:
                    if len(line.strip()) > 0:
                        if line.strip()[0] == ";":
                            continue
                        # Proceed through base stats file in order of non-empty non-comment lines.
                        # Any layout changes would require this to change.
                        # Probably a better way of doing this.
                        # This will allow for differences in empty lines and comments at least.
                        # No case statement because python just added those relatively recently.
                        # Don't wanna mess up people with slightly older versions.
                        # Also no fallback needed.
                        if j == 0:
                            self.bsConstant(line, i)
                        elif j == 1:
                            self.bsStats(line, i)
                        elif j == 2:
                            self.bsTypes(line, i)
                        elif j == 3:
                            self.bsCatchRate(line, i)
                        elif j == 4:
                            self.bsBaseXP(line, i)
                        elif j == 5:
                            self.bsItems(line, i)
                        elif j == 6:
                            self.bsGenderRatio(line, i)
                        elif j == 7:
                            self.bsUnknown(line, i)
                        elif j == 8:
                            self.bsStepCycle(line, i)
                        elif j == 9:
                            self.bsUnknown2(line, i)
                        elif j == 10:
                            self.bsFrontDimensions(line, i)
                        elif j == 11:
                            self.bsUnusedFrontBack(line, i)
                        elif j == 12:
                            self.bsGrowthRate(line, i)
                        elif j == 13:
                            self.bsEggGroups(line, i)
                        elif j == 14:
                            self.bsTMHMList(line, i)
                        j += 1

    def bsConstant(self, line, i):
        return None

    def bsStats(self, line, i):
        array = line.split("db ")
        array = array[1]
        array = array.split(",")
        self.pokemonData[i]["Stats"] = {}
        for index, stat in enumerate(baseStatFileBaseStatOrder):
            self.pokemonData[i]["Stats"][stat] = array[index].strip()

    def bsTypes(self, line, i):
        array = line.split("db ")
        array = array[1]
        array = array.split(", ")
        self.pokemonData[i]["Types"] = []
        for entry in array:
            self.pokemonData[i]["Types"].append(
                entry.replace("; type", "").strip()
            )

    def bsCatchRate(self, line, i):
        catchRate = line.split("db ")
        catchRate = catchRate[1].split(" ")
        catchRate = catchRate[0].strip()
        self.pokemonData[i]["Catch Rate"] = catchRate

    def bsBaseXP(self, line, i):
        baseXP = line.split("db ")
        baseXP = baseXP[1].split(" ")
        baseXP = baseXP[0].strip()
        self.pokemonData[i]["Base XP"] = baseXP

    def bsItems(self, line, i):
        array = line.split("db ")
        array = array[1]
        array = array.split(", ")
        self.pokemonData[i]["Held Items"] = []
        for entry in array:
            if "NO_ITEM" not in entry:
                self.pokemonData[i]["Held Items"].append(
                    entry.replace("; items", "").replace("\n", "")
                )

    def bsGenderRatio(self, line, i):
        gender = line.split("db ")
        gender = gender[1].split(" ")
        gender = gender[0].strip()
        self.pokemonData[i]["Gender Ratio"] = gender

    def bsUnknown(self, line, i):
        return None

    def bsStepCycle(self, line, i):
        stepCycle = line.split("db ")
        stepCycle = stepCycle[1].split(" ")
        stepCycle = stepCycle[0].strip()
        self.pokemonData[i]["Step Cycle"] = stepCycle

    def bsUnknown2(self, line, i):
        return None

    def bsFrontDimensions(self, line, i):
        frontDimensionsFile = line.split("INCBIN ")
        frontDimensionsFile = frontDimensionsFile[1]
        frontDimensionsFile = frontDimensionsFile.replace('"', "")
        self.pokemonData[i]["Front Dimensions File"] = frontDimensionsFile

    def bsUnusedFrontBack(self, line, i):
        return None

    def bsGrowthRate(self, line, i):
        growthRate = line.split("db ")
        growthRate = growthRate[1].split(" ")
        growthRate = growthRate[0].strip()
        self.pokemonData[i]["Growth Rate"] = growthRate

    def bsEggGroups(self, line, i):
        eggGroups = []
        array = line.split("dn ")
        array = array[1]
        array = array.split(", ")
        for entry in array:
            eggGroups.append(entry.replace("; egg groups", "").strip())
        self.pokemonData[i]["Egg Groups"] = eggGroups

    def bsTMHMList(self, line, i):
        tmList = []
        array = line.split("tmhm")
        array = array[1]
        array = array.split(", ")
        for entry in array:
            tmList.append(entry.strip())
        self.pokemonData[i]["TM HM List"] = tmList

    def getEvosAttacksPointers(self):
        files = ['evosAttacksKanto', 'evosAttacksJohto']
        i = 0
        for fName in files:
            with open(pokeDataFiles[fName], "r") as f:
                for line in f:
                    if ".IndirectEnd::" in line:
                        break
                    if "dw" in line:
                        evosAttacksPointer = line.split("dw ")
                        evosAttacksPointer = evosAttacksPointer[1].strip()
                        self.pokemonData[i]["Evos Attacks Pointer"] = evosAttacksPointer
                        i += 1

    def getEvosAttacks(self):
        files = ['evosAttacksKanto', 'evosAttacksJohto']
        evosAttacksData = {}
        for fName in files:
            ready = False
            with open(pokeDataFiles[fName], "r") as f:
                curPoke = None
                processOrder = ["Evos", "Attacks"]
                currentStep = 0
                for line in f:
                    if ready:
                        # Ignore comment lines
                        if line[0] == ";":
                            continue
                        # Go line by line, looking for startpoint.
                        if curPoke is None:
                            if "EvosAttacks" in line:
                                # Get the current pointer
                                curPoke = line.strip().replace(":", "")
                                # Mark it to start processing from step 1
                                currentStep = 0
                                # Setup Dictionaries
                                evosAttacksData[curPoke] = {}
                                evosAttacksData[curPoke]["Evos"] = []
                                evosAttacksData[curPoke]["Attacks"] = []
                        # Mark end of section
                        if "db 0" in line:
                            if currentStep + 1 == len(processOrder):
                                # It's done with all steps
                                curPoke = None
                            else:
                                # Start Next Step
                                currentStep += 1
                        elif "dbbw" in line or "dbbbw" in line:
                            evoData = []
                            if "dbbw" in line:
                                evoData = line.split("dbbw")
                            if "dbbbw" in line:
                                evoData = line.split("dbbbw")
                            evoData = evoData[1]
                            evoData = evoData.split(",")
                            dataOrder = evoMethodDataOrder[evoData[0].strip()]
                            curEvo = {"Method": evoData[0].strip()}
                            for i, datum in enumerate(dataOrder):
                                # it's equal to +1 since index 0 is the method.
                                curEvo[datum] = evoData[i + 1].strip()
                            evosAttacksData[curPoke]["Evos"].append(curEvo)
                        if "dbw" in line:
                            attackData = line.split("dbw")
                            attackData = attackData[1]
                            attackData = attackData.split(", ")
                            curAttack = {}
                            curAttack["Level"] = attackData[0].strip()
                            curAttack["Move"] = attackData[1].strip()
                            evosAttacksData[curPoke]["Attacks"].append(curAttack)
                    elif ".IndirectEnd" in line:
                        ready = True 
        for i, pokemon in enumerate(self.pokemonData):
            if "Evos Attacks Pointer" in pokemon:
                if pokemon["Evos Attacks Pointer"] in evosAttacksData:
                    evos = evosAttacksData[pokemon["Evos Attacks Pointer"]]["Evos"]
                    attacks = evosAttacksData[pokemon["Evos Attacks Pointer"]]["Attacks"]
                    self.pokemonData[i]["Evolutions"] = evos
                    self.pokemonData[i]["Level Up Moves"] = attacks
                else:
                    print("ERROR No Evos Attacks Found for " + pokemon["Constant"])

            else:
                print("ERROR No Evos Attacks Pointers Found for " + pokemon["Constant"])

    def getEggMovePointers(self):
        files = ["eggMovesKanto", "eggMovesJohto"]
        i = 0
        for fName in files:
            with open(pokeDataFiles[fName], "r") as f:
                for line in f:
                    if "dw" in line:
                        eggMovePointer = line.split("dw")
                        eggMovePointer = eggMovePointer[1].strip()
                        self.pokemonData[i]["Egg Move Pointer"] = eggMovePointer
                        i += 1
                    if ".IndirectEnd" in line:
                        break

    def getEggMoves(self):
        eggMoveData = {}
        files = ["eggMovesKanto", "eggMovesJohto"]
        for fName in files:
            with open(pokeDataFiles[fName], "r") as f:
                curPoke = None
                for line in f:
                    # Ignore comment lines
                    if line[0] == ";":
                        continue
                    # Go line by line, looking for startpoint.
                    if curPoke is None:
                        if "EggMoves" in line:
                            # Get the current pointer
                            curPoke = line.strip().replace(":", "")
                            # Create Array for egg moves
                            eggMoveData[curPoke] = []
                    # Mark end of section
                    if "dw -1 " in line:
                        curPoke = None
                    elif "dw" in line:
                        eggMove = line.split("dw")
                        eggMove = eggMove[1]
                        eggMoveData[curPoke].append(eggMove.strip())
        for i, pokemon in enumerate(self.pokemonData):
            if "Egg Move Pointer" in pokemon:
                if pokemon["Egg Move Pointer"] in eggMoveData:
                    self.pokemonData[i]["Egg Moves"] = eggMoveData[pokemon["Egg Move Pointer"]]
                # else:
                    # print("ERROR No Egg Moves Found for " + pokemon["Constant"])

            else:
                print("ERROR No Egg Move Pointers Found for " + pokemon["Constant"])

    def getMenuIcons(self):
        with open(pokeDataFiles["iconPointers"], "r") as f:
            i = 0
            ready = False
            for line in f:
                if ready:
                    if "dw" in line:
                        if "NullIcon" in line:
                            continue
                        menuIcon = line.split("dw")
                        menuIcon = menuIcon[1].split("; ")
                        menuIcon = menuIcon[0].strip()
                        self.pokemonData[i]["Menu Icon"] = menuIcon
                        i += 1
                elif "IconPointers" in line:
                    ready = True

    def getMenuPals(self):
        with open(pokeDataFiles["menuIconPals"], "r") as f:
            i = 0
            ready = False
            for line in f:
                if ready:
                    if "icon_pals" in line:
                        menuIcon = line.split("icon_pals")
                        menuIcon = menuIcon[1].split("; ")
                        menuIcon = menuIcon[0].strip()
                        menuIcon = menuIcon.split(",")
                        self.pokemonData[i]["Menu Icon Palettes"] = [
                            menuIcon[0].strip(),
                            menuIcon[1].strip()
                        ]
                        i += 1
                elif "MonMenuIconPals" in line:
                    ready = True


    def getDexEntryPointers(self):
        with open(pokeDataFiles["dexEntryPointers"], "r") as f:
            i = 0
            for line in f:
                if "dba" in line:
                    dexEntryPointer = line.split("dba")
                    dexEntryPointer = dexEntryPointer[1].strip()
                    self.pokemonData[i]["Dex Entry Pointer"] = dexEntryPointer
                    i += 1

    def getDexEntryFiles(self):
        dexEntryFileData = {}
        with open(pokeDataFiles["dexEntries"], "r") as f:
            for line in f:
                if "PokedexEntry" in line:
                    entryData = line.split("::")
                    pointer = entryData[0]
                    entryData = entryData[1].strip()
                    entryData = entryData.split("INCLUDE ")
                    file = entryData[1].replace('"', "").strip()
                    dexEntryFileData[pointer] = file
        for i, pokemon in enumerate(self.pokemonData):
            if "Dex Entry Pointer" in pokemon:
                if pokemon["Dex Entry Pointer"] in dexEntryFileData:
                    entryFile = dexEntryFileData[pokemon["Dex Entry Pointer"]]
                    self.pokemonData[i]["Dex Entry File"] = "../" + entryFile
                else:
                    print("ERROR No Dex Entry Found for " + pokemon["Constant"])

            else:
                print("ERROR No Dex Entry Found for " + pokemon["Constant"])

    def processDexEntryFiles(self):
        for i, pokemon in enumerate(self.pokemonData):
            if "Dex Entry File" not in pokemon:
                print("ERROR, no Dex Entry File Known for " + pokemon["Constant"])
                continue
            with open(pokemon["Dex Entry File"], "r") as f:
                dexData = {}
                j = 0
                dexTextArray = []
                for line in f:
                    if len(line.strip()) > 0:
                        if line.strip()[0] == ";":
                            continue
                        if j == 0:
                            species = line.split("db ")
                            species = species[1]
                            species = species.split("@")
                            species = species[0].replace('"', "")
                            dexData["Species Name"] = species.strip()
                        if j == 1:
                            sizeData = line.split("dw ")
                            sizeData = sizeData[1]
                            sizeData = sizeData.split(",")
                            height = sizeData[0].strip()
                            weight = sizeData[1].split(";")
                            weight = weight[0].strip()
                            dexData["Height"] = height
                            dexData["Weight"] = weight
                        if j > 1:
                            dexText = line.split('"')
                            dexText = dexText[1].replace("@", "")
                            dexText = dexText.strip()
                            dexTextArray.append(dexText)
                        j += 1
                dexEntryArray = [
                    "\n".join(dexTextArray[0:2]),
                    "\n".join(dexTextArray[3:])
                ]
                dexData["Pokedex Entry"] = "\f".join(dexEntryArray)
                self.pokemonData[i]["Species Name"] = dexData["Species Name"]
                self.pokemonData[i]["Height"] = dexData["Height"]
                self.pokemonData[i]["Weight"] = dexData["Weight"]
                self.pokemonData[i]["Pokedex Entry"] = dexData["Pokedex Entry"]

    def getDexOrderNew(self):
        with open(pokeDataFiles["dexOrderNew"], "r") as f:
            dexOrderNew = {}
            dexNumberNew = 1
            for line in f:
                if "dw" in line:
                    dexPoke = line.split("dw")
                    dexPoke = dexPoke[1].split("; ")
                    dexPoke = dexPoke[0].strip()
                    dexOrderNew[dexPoke] = dexNumberNew
                    dexNumberNew += 1
            for i, pokemon in enumerate(self.pokemonData):
                self.pokemonData[i]["Dex Number (New)"] = dexOrderNew[pokemon["Constant"]]

    def getDexOrderAlpha(self):
        # Why did I even have this
        # with open(pokeDataFiles["dexOrderAlpha"], "r") as f:
        #     dexOrderAlpha = {}
        #     dexNumberAlpha = 1
        #     for line in f:
        #         if "db" in line:
        #             dexPoke = line.split("db ")
        #             dexPoke = dexPoke[1].split("; ")
        #             dexPoke = dexPoke[0].strip()
        #             dexOrderAlpha[dexPoke] = dexNumberAlpha
        #             dexNumberAlpha += 1
        #     for i, pokemon in enumerate(self.pokemonData):
        #         self.pokemonData[i]["Dex Number (Alpha)"] = dexOrderAlpha[pokemon["Constant"]]
        return

    def getPicPointers(self):
        with open(pokeDataFiles["picPointers"], "r") as f:
            i = 0
            for line in f:
                if "NUM_POKEMON" in line or i >= len(self.pokemonData):
                    break
                # Messy Unown Handling
                elif "dbw " in line:
                    if "Front Pic Pointer" in self.pokemonData[i]:
                        self.pokemonData[i]["Back Pic Pointer"] = "UnownBackPic"
                    else:
                        self.pokemonData[i]["Front Pic Pointer"] = "UnownFrontPic"
                elif "dba " in line:
                    picPointer = line.split("dba ")
                    picPointer = picPointer[1].strip()
                    if "Front Pic Pointer" in self.pokemonData[i]:
                        self.pokemonData[i]["Back Pic Pointer"] = picPointer
                    else:
                        self.pokemonData[i]["Front Pic Pointer"] = picPointer
                if "Front Pic Pointer" in self.pokemonData[i]:
                    if "Back Pic Pointer" in self.pokemonData[i]:
                        i += 1

    def getPalettes(self):
        with open(pokeDataFiles["pokePalettes"], "r") as f:
            i = 0
            for line in f:
                if "assert_table_length NUM_POKEMON" in line or i >= len(self.pokemonData):
                    break
                if line[0] == ";":
                    continue
                if "INC" in line:
                    if "normal.pal" in line:
                        normal = line.split("INCLUDE ")
                        normal = normal[1]
                        normal = normal.split(";")
                        normal = normal[0]
                        normal = normal.replace('"', "").split()
                        self.pokemonData[i]["Normal Palette"] = normal
                    elif "front.gbcpal" in line:
                        front = line.split("INCBIN ")
                        front = front[1]
                        front = front.split(",")
                        front = front[0]
                        front = front.replace('"', "").split()
                        self.pokemonData[i]["Normal Palette"] = front
                    elif "shiny.pal" in line:
                        shiny = line.split("INCLUDE ")
                        shiny = shiny[1]
                        shiny = shiny.replace('"', "").split()
                        self.pokemonData[i]["Shiny Palette"] = shiny
                if "Normal Palette" in self.pokemonData[i]:
                    if "Shiny Palette" in self.pokemonData[i]:
                        i += 1

    def getPics(self):
        picData = {}
        with open(pokeDataFiles["pics"], "r") as f:
            for line in f:
                if "Front" in line or "Back" in line:
                    picLine = line.split(":")
                    pointer = picLine[0]
                    file = picLine[1]
                    file = file.split("INCBIN ")
                    file = file[1]
                    file = file.split(".")
                    file = file[0].strip()
                    picData[pointer] = "../" + file.replace('"', "") + ".png" 
        for i, poke in enumerate(self.pokemonData):
            if poke["Front Pic Pointer"] in picData:
                self.pokemonData[i]["Front Pic"] = picData[poke["Front Pic Pointer"]]
            if poke["Back Pic Pointer"] in picData:
                self.pokemonData[i]["Back Pic"] = picData[poke["Back Pic Pointer"]]


# pokemon = PokemonDataBuilder()
# pokemon.buildPokemonData()

# moves = MoveDataBuilder()
# moves.buildMoveData()

items = ItemDataBuilder()
items.buildItemData()

for item in items.itemData:
    if item["Constant"] == "NO_ITEM":
        continue
    if "Effect" not in item:
        item["Effect"] = "NoEffect"
    item = item_data.Item(
        constant = item["Constant"],
        name = item["Name"],
        price = item["Price"],
        held_effect = item["Held Effect"],
        parameter = item["Parameter"],
        item_property = item["Property"],
        pocket = item["Pocket"],
        field_menu = item["Field Menu"],
        battle_menu = item["Battle Menu"],
        description = item["Description"],
        effect = item["Effect"]
    )
    item.generate_yaml()

# for move in moves.moveData:
#     if move["Constant"] == "NO_MOVE":
#         continue
#     move['Type'] = move['Type'].title().replace('_Type', '')
#     move = move_data.Move(
#         constant = move['Constant'],
#         name = move['Name'],
#         animation = move['Animation'],
#         effect = move['Effect'],
#         power = move['Power'],
#         move_type = move['Type'],
#         category = move['Category'],
#         accuracy = move["Accuracy"],
#         pp = move["PP"],
#         effect_chance = move["Effect Chance"],
#         description = move["Description"],
#     )
#     move.generate_yaml()

# for poke in pokemon.pokemonData:
#     poke["Stats"]  = {
#         'hp': poke["Stats"]["HP"],
#         'attack': poke["Stats"]["ATK"],
#         'defense': poke["Stats"]["DEF"],
#         'sp_attack': poke["Stats"]["SAT"],
#         'sp_defense': poke["Stats"]["SDF"],
#         'speed': poke['Stats']["SPD"]
#     }
#     poke['Types'][0] = poke['Types'][0].title().replace("_Type", "")
#     poke['Types'][1] = poke['Types'][1].title().replace("_Type", "")
#     if poke['Types'][0] == poke['Types'][1]:
#         poke['Types'].pop(1)
#     eggs = []
#     for group in poke["Egg Groups"]:
#         group = group.replace("EGG_", "").replace("_"," ")
#         eggs.append(group.title())
#     eggs =  list(dict.fromkeys(eggs))
#     if "Egg Moves" not in poke:
#         poke["Egg Moves"] = []
#     level_ups = []
#     for move in poke["Level Up Moves"]:
#         level_ups.append((move["Level"], move["Move"]))
#     evolutions = []
#     if "Evolutions" in poke:
#         for evolu in poke["Evolutions"]:
#             evo = evolu
#             method = evo["Method"].replace("EVOLVE_","").title()
#             method = method.replace("Level", "Level-Up")
#             evo["Method"] = method
#             evolutions.append(evo)
#             # print(evo)
        
#     mon = pokemon_data.Pokemon(
#         constant = poke["Constant"],
#         name = poke['Name'],
#         stats = poke["Stats"],
#         types = poke["Types"],
#         catch_rate = poke["Catch Rate"],
#         base_xp = poke["Base XP"],
#         growth_rate = poke["Growth Rate"][7:].replace("_","-").title(),
#         egg_step_cycle = poke["Step Cycle"],
#         gender_ratio = poke["Gender Ratio"].replace("GENDER_","").replace("F","").replace("_",".").title(),
#         egg_groups = eggs,
#         held_items = poke["Held Items"],
#         level_up_moves = level_ups,
#         egg_moves = poke["Egg Moves"],
#         evolutions = poke["Evolutions"],
#         taught_moves = poke["TM HM List"],
#         species = poke["Species Name"],
#         height = poke["Height"],
#         weight = poke["Weight"],
#         icon = poke["Menu Icon"],
#         icon_pals = poke["Menu Icon Palettes"],
#         flavor_text = poke["Pokedex Entry"],
#         normal_palette = poke["Normal Palette"],
#         shiny_palette = poke["Shiny Palette"]
#     )
#     mon.generate_yaml()