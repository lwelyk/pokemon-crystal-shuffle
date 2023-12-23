import operator
import re
import yaml
from . import common, yaml_loaders
import csv
import os
from dataclasses import dataclass

# Be a file or something later, just here for testing and setup
flags = {
    "SpecialStat": False,
    "PhysicalSpecialSplit": True
}
# Special Stat True will revert back to gen 1 style mono stat here, which idk how I'll implement or if.
# I'd modify attack and defense to be the same and modify move effects to raise/lower both at once.
# No idea how easy/hard this would be. Probably not too bad?
# I personally don't have a great interest in it. this is for me to ref later.

# PhysicalSpecialSplit when false would just modify all moves to use their type's old physical or
# special deliniation, so technically it would still be there, just every attack would be defined
# by type instead of move.

@dataclass
class Pokemon:
    constant: str
    name: str
    base_stats: dict
    types: list
    catch_rate: int
    base_xp: int
    growth_rate: str
    gender_ratio: str
    egg_step_cycle: str
    level_up_moves: list
    species: str
    height: int
    weight: int
    icon: str
    icon_pals: list
    pokedex_entry: str
    normal_palette: str
    shiny_palette: str
    held_items: list = []
    egg_groups: list = []
    taught_moves: list = []
    egg_moves: list = []
    evolutions: list = []
    
    constant = property(operator.attrgetter('_constant'))
    
    @constant.setter
    def constant(self, const):
        self._constant = common.check_constant(const)

    name = property(operator.attrgetter('_name'))
    
    @name.setter
    def name(self, name):
        self._name = common.check_string(name, 10, "Pokemon Names")

    base_stats = property(operator.attrgetter('_base_stats'))

    @base_stats.setter
    def base_stats(self, base_stats):
        if not base_stats:
            raise Exception("Pokemon need stats.")
        if type(base_stats) != dict:
            raise Exception("Pokemon stats should be a dictionary.")
        # Should specify this elsewhere.
        stats_list = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'] 
        for stat_name in stats_list:
            if stat_name not in base_stats:
                raise Exception("Pokemon stats missing " + stat_name)
        for stat, value in base_stats.items():
            value = common.check_number(value, 1, 255, "Pokemon Stat")
        self.hp = int(base_stats["hp"])
        self.attack = int(base_stats["attack"])
        self.defense = int(base_stats["defense"])
        self.sp_attack = int(base_stats["sp_attack"])
        self.sp_defense = int(base_stats["sp_defense"])
        self.speed = int(base_stats["speed"])
    
    @base_stats.getter
    def base_stats(self):
        bs = {
            "hp" : self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "sp_attack": self.sp_attack,
            "sp_defense": self.sp_defense,
            "speed": self.speed
        }
        return bs

    types = property(operator.attrgetter('_types'))
    
    @types.setter
    def types(self, types):
        if type(types) != list:
            print("You should pass types as a list.")
            types = [types]
        for poke_type in types:
            common.validate_type(poke_type)
        self._types = types
        
    growth_rate = property(operator.attrgetter('_growth_rate'))
    
    @growth_rate.setter
    def growth_rate(self, growth_rate):
        # Temporary list
        growth_rates = ["Medium-Fast", "Slightly-Fast", "Slightly-Slow", "Medium-Slow", "Fast", "Slow"]
        if type(growth_rate) != str:
            raise Exception("Growth Rate should be a string. You provided " + str(growth_rate))
        if growth_rate not in growth_rates:
            raise Exception(growth_rate + " is not a valid growth rate.")
        self._growth_rate = growth_rate
        
    catch_rate = property(operator.attrgetter('_catch_rate'))
    
    @catch_rate.setter
    def catch_rate(self, catch_rate):
        self._catch_rate = common.check_number(catch_rate, 1, 255, "Catch Rate")
    
    base_xp = property(operator.attrgetter('_base_xp'))
    
    @base_xp.setter
    def base_xp(self, base_xp):
        self._base_xp = common.check_number(base_xp, 1, 255, "Base XP")

    egg_step_cycle = property(operator.attrgetter('_egg_step_cycle'))
    
    @egg_step_cycle.setter
    def egg_step_cycle(self, egg_step_cycle):
        self._egg_step_cycle = common.check_number(egg_step_cycle, 1, 255, "Egg Step Cycle")
    
    gender_ratio = property(operator.attrgetter('_gender_ratio'))
    
    @gender_ratio.setter
    def gender_ratio(self, gender_ratio):
        # Put this here for now.
        # Just making it the female percentage.
        ratios = ['0', '12.5', '25', '50', '75', '100', 'Unknown']
        if str(gender_ratio) not in ratios:
            raise Exception("Sorry you have provided an invalid gender ratio of " + str(gender_ratio))
        self._gender_ratio = gender_ratio

    egg_groups = property(operator.attrgetter('_egg_groups'))
    
    @egg_groups.setter
    def egg_groups(self, egg_groups):
        # Putting this here for now, just the constants
        egg_group_list = [
            'Monster', 'Water 1', 'Bug', 'Flying', 
            'Ground', 'Fairy', 'Plant', 'Humanshape', 
            'Water 3', 'Mineral', 'Indeterminate', 
            'Water 2', 'Ditto', 'Dragon', 'None'
        ]
        if type(egg_groups) != list:
            if egg_groups in egg_group_list:
                egg_groups = [egg_groups]
                print("Please pass egg groups as a list, the one you passed is valid so converting for you.")
            else:
                print("Please pass egg groups as a list, and make sure the group is valid.")
        for group in egg_groups:
            if group not in egg_group_list:
                raise Exception("Invalid egg group provided, you gave '" + str(group) + "'.")
        self._egg_groups = egg_groups
            
    held_items = property(operator.attrgetter('_held_items'))
    
    @held_items.setter
    def held_items(self, held_items):
        # Add checks later once item objects exist.
        self._held_items = held_items

    level_up_moves = property(operator.attrgetter('_level_up_moves'))
    
    @level_up_moves.setter
    def level_up_moves(self, level_up_moves):
        # Simple for now, no moves setup yet.
        if len(level_up_moves) < 1:
            raise Exception("Sorry, a Pokemon has to have a level up move.")
        for level_up_move in level_up_moves:
            if type(level_up_move) is not tuple:
                raise Exception("You need to provide each level up move as a tuple.")
            if not str(level_up_move[0]).isnumeric():
                raise Exception("The first element in the tuple for level up moves must be the level")
            if type(level_up_move[1]) is not str:
                raise Exception("The second element in the tuple for level up moves must be the move.")
            # check for vaild moves here
        self._level_up_moves = level_up_moves
    
    taught_moves = property(operator.attrgetter('_taught_moves'))
    
    @taught_moves.setter
    def taught_moves(self, taught_moves):
        for taught_move in taught_moves:
            if type(taught_move) is not str:
                raise Exception("Each Taught move must be a string.")
            # check for valid moves here.
        self._taught_moves = taught_moves
    
    egg_moves = property(operator.attrgetter('_egg_moves'))
    
    @egg_moves.setter
    def egg_moves(self, egg_moves):
        for egg_move in egg_moves:
            if type(egg_move) is not str:
                raise Exception("Each egg move must be a string.")
            # check for valid moves here.
        self._egg_moves = egg_moves
    
    evolutions = property(operator.attrgetter('_evolutions'))
    
    @evolutions.setter
    def evolutions(self, evolutions):
        # Temporary hold of evo method lists
        evolution_methods = {
            "Level-Up": ["Level"],
            "Item": ["Used Item"],
            "Trade": [],
            "Happiness": ["Time"],
            "Stat": ["Level", "Stat Relationship"]
        }
        for evolution in evolutions: 
            if "Method" not in evolution:
                raise Exception("You must provide a method of evolution.")
            if evolution["Method"] not in evolution_methods:
                raise Exception("Invalid evolution method " + evolution["Method"] + " provided.")
            if "Species" not in evolution:
                raise Exception("You have to provide a species to evolve to.")
            for req in evolution_methods[evolution["Method"]]:
                if req not in evolution:
                    raise Exception("Evolution Method " + evolution["Method"] + " requires " + req + ", which is missing.")
        # Need some way to ensure the species is real, maybe in the Pokedex methods.
        self._evolutions = evolutions

    species = property(operator.attrgetter('_species'))
    
    @species.setter
    def species(self, species):
         self._species = common.check_string(species, 11, "Species Name")
        
    height = property(operator.attrgetter('_height'))
    
    @height.setter
    def height(self, height):
        # idk, I'll figure out how I want to store this later.
        self._height = int(height)
    
    weight = property(operator.attrgetter('_weight'))
    
    @weight.setter
    def weight(self, weight):
        # idk, I'll figure out how I want to store this later.
        self._weight = int(weight)
    
    icon = property(operator.attrgetter('_icon'))
    
    @icon.setter
    def icon(self, icon):
        if not icon:
            raise Exception("Pokemon need an icon.")
        # Not sure how I want to handle this yet.
        self._icon = icon
        
    icon_pals = property(operator.attrgetter('_icon_pals'))
    
    @icon_pals.setter
    def icon_pals(self, icon_pals):
        # Temporary home of palettes list
        pals = ["RED", "BLUE", "GREEN", "BROWN", "PINK", "GRAY", "TEAL", "PURPLE"]
        for pal in icon_pals:
            if pal not in pals:
                raise Exception("Provided pal " + str(pal) + " is invalid")
        self._icon_pals = icon_pals
    
    pokedex_entry = property(operator.attrgetter('_pokedex_entry'))
    
    @pokedex_entry.setter
    def pokedex_entry(self, pokedex_entry):
        # update later.
        self._pokedex_entry = pokedex_entry
        
    normal_palette = property(operator.attrgetter('_normal_palette'))
    
    @normal_palette.setter
    def normal_palette(self, normal_palette):
        # update later
        self._normal_palette = normal_palette
        
    shiny_palette = property(operator.attrgetter('_shiny_palette'))
    
    @shiny_palette.setter
    def shiny_palette(self, shiny_palette):
        # update later
        self._shiny_palette = shiny_palette
    
    def generate_yml(self):
        level_ups =[]
        for move in self.level_up_moves:
            level_ups.append({int(move[0]) : move[1]})
        yml = {
            "constant": self.constant,
            "name": self.name,
            "types": self.types,
            "base_stats": {
                "hp": self.hp,
                "attack": self.attack,
                "defense": self.defense,
                "speed": self.speed,
                "sp_attack": self.sp_attack,
                "sp_defense": self.sp_defense
            },
            "growth_rate": self.growth_rate,
            "catch_rate": self.catch_rate,
            "base_xp": self.base_xp
        }
        if self.held_items:
            yml["held_items"] = self.held_items
        yml["gender_ratio"] = self.gender_ratio
        yml["egg_step_cycle"] = self.egg_step_cycle
        yml["egg_groups"] = self.egg_groups
        if len(self.evolutions) > 0:
           yml["evolutions"] = self.evolutions
        yml["species"] = self.species
        yml["height"] = self.height
        yml["weight"] = self.weight
        yml["pokedex_entry"] = self.pokedex_entry
        yml["icon"] = self.icon
        yml["icon_pals"] = self.icon_pals
        yml["moves"] = {}
        yml["moves"]["level_up"] = level_ups
        if self.taught_moves:
            yml["moves"]["taught_moves"] = self.taught_moves
        if self.egg_moves:
            yml["moves"]["egg_moves"] = self.egg_moves
        self.yml = yml
    
    def write_yml(self):
        if len(self.yml) < 2:
            raise Exception("You need yml to be set before you can write the file.")
        file_name = 'pokemon/' + self.constant.lower() + '.yml'
        with open(file_name, 'w') as file:
            documents = yaml.dump(self.yml, file, sort_keys=False)

class Pokedex:
    def __init__(self):
        self.pokemon_list = {}
        self.dex_order = []
        self.new_dex_order = []
    
    def add_pokemon(self, pokemon):
        self.pokemon_list.append(pokemon)
    
    def load_pokedex_file(self, file):
        f = open(file, 'r')
        reader = csv.DictReader(f)
        dex = {}
        new_dex = {}
        for row in reader:
            self.pokemon_list[row["constant"]] = {}
            dex[int(row["dex_order"])] = row["constant"]
            new_dex[int(row["new_dex_order"])] = row["constant"]
        self.dex_order = [value for key, value in sorted(dex.items())]
        print(self.dex_order)
        self.new_dex_order = [value for key, value in sorted(new_dex.items())]
        print(self.new_dex_order)
    
    def create_pokemon_objects(self):
        if self.pokemon_list:
            yl = yaml_loaders.YLoader()
            for pokemon in self.pokemon_list:
                poke = yl.poke_from_yml(pokemon)
                poke.generate_yml()
                poke.write_yml()
                self.pokemon_list[pokemon] = poke
