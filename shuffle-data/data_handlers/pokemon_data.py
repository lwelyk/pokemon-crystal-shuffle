import operator
import re
import yaml
from . import common

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
class Pokemon:
    def __init__(
        self,
        constant,
        name,
        stats,
        types,
        catch_rate,
        base_xp,
        growth_rate,
        gender_ratio,
        egg_step_cycle,
        level_up_moves,
        species,
        height,
        weight,
        icon,
        icon_pals,
        flavor_text,
        normal_palette,
        shiny_palette,
        shape="",
        held_items=[],
        egg_groups=[],
        taught_moves=[],
        egg_moves= [],
        evolutions=[]
        # pokedex_numbers={},
        # front_sprite,
        # back_sprite  
      ):
        self.constant = constant
        self.name = name
        self.stats = stats
        self.types = types
        self.catch_rate = catch_rate
        self.base_xp = base_xp
        self.growth_rate = growth_rate
        self.gender_ratio = gender_ratio
        self.egg_step_cycle = egg_step_cycle
        self.level_up_moves = level_up_moves
        self.species = species
        self.height = height
        self.weight = weight
        self.icon = icon
        self.icon_pals = icon_pals
        self.flavor_text = flavor_text
        self.normal_palette = normal_palette
        self.shiny_palette = shiny_palette
        self.shape = shape
        self.held_items = held_items
        self.egg_groups = egg_groups
        self.taught_moves = taught_moves
        self.egg_moves = egg_moves
        self.evolutions = evolutions
    
    constant = property(operator.attrgetter('_constant'))
    
    @constant.setter
    def constant(self, const):
        if not const: 
            raise Exception ("Pokemon need a constant.")
        self._constant = common.check_constant(const)

    name = property(operator.attrgetter('_name'))
    
    @name.setter
    def name(self, name):
        if not name:
            raise Exception("Pokemon need a name.")
        self._name = common.check_string(name, 10, "Pokemon Names")

    stats = property(operator.attrgetter('_stats'))

    @stats.setter
    def stats(self, stats):
        if not stats:
            raise Exception("Pokemon need stats.")
        if type(stats) != dict:
            raise Exception("Pokemon stats should be a dictionary.")
        # Should specify this elsewhere.
        stats_list = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'] 
        for stat_name in stats_list:
            if stat_name not in stats:
                raise Exception("Pokemon stats missing " + stat_name)
        for stat, value in stats.items():
            value = common.check_number(value, 1, 255, "Pokemon Stat")
        self.hp = int(stats["hp"])
        self.attack = int(stats["attack"])
        self.defense = int(stats["defense"])
        self.sp_attack = int(stats["sp_attack"])
        self.sp_defense = int(stats["sp_defense"])
        self.speed = int(stats["speed"])

    types = property(operator.attrgetter('_types'))
    
    @types.setter
    def types(self, types):
        # Temporarily just having a list here, will pull from types.yml later
        type_list = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]
        if not types:
            raise Exception("Pokemon need types.")
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
        if not growth_rate:
            raise Exception("Pokemon need a growth rate.")
        if type(growth_rate) != str:
            raise Exception("Growth Rate should be a string. You provided " + str(growth_rate))
        if growth_rate not in growth_rates:
            raise Exception(growth_rate + " is not a valid growth rate.")
        self._growth_rate = growth_rate
        
    catch_rate = property(operator.attrgetter('_catch_rate'))
    
    @catch_rate.setter
    def catch_rate(self, catch_rate):
        if not catch_rate:
            raise Exception("Pokemon need a catch rate.")
        self._catch_rate = common.check_number(catch_rate, 1, 255, "Catch Rate")
    
    base_xp = property(operator.attrgetter('_base_xp'))
    
    @base_xp.setter
    def base_xp(self, base_xp):
        if not base_xp:
            raise Exception("Pokemon need a base xp.")
        self._base_xp = common.check_number(base_xp, 1, 255, "Base XP")

    egg_step_cycle = property(operator.attrgetter('_egg_step_cycle'))
    
    @egg_step_cycle.setter
    def egg_step_cycle(self, egg_step_cycle):
        if not egg_step_cycle:
            raise Exception("Pokemon need an egg_step_cycle.")
        self._egg_step_cycle = common.check_number(egg_step_cycle, 1, 255, "Egg Step Cycle")
    
    gender_ratio = property(operator.attrgetter('_gender_ratio'))
    
    @gender_ratio.setter
    def gender_ratio(self, gender_ratio):
        # Put this here for now.
        # Just making it the female percentage.
        ratios = ['0', '12.5', '25', '50', '75', '100', 'Unknown']
        if not gender_ratio:
            raise Exception("Sorry, the Pokemon world has not yet abolished gender. Please provide a ratio.")
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
        if not egg_groups:
            raise Exception("Pokemon need to be given an egg group.")
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
        if type(level_up_moves) is not list:
            raise Exception("Sorry, you need to provide a list of level up moves.")
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
        if type(taught_moves) is not list:
            raise Exception("Sorry, taught moves needs to be a list.")
        for taught_move in taught_moves:
            if type(taught_move) is not str:
                raise Exception("Each Taught move must be a string.")
            # check for valid moves here.
        self._taught_moves = taught_moves
    
    egg_moves = property(operator.attrgetter('_egg_moves'))
    
    @egg_moves.setter
    def egg_moves(self, egg_moves):
        if type(egg_moves) is not list:
            raise Exception("Sorry, egg moves needs to be a list.")
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
        if type(evolutions) is not list:
            raise Exception("Evolutions must be passed as a list.")
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
        if not(species):
            raise Exception("Pokemon need a species name.")
        if type(species) is not str:
            raise Exception("Species should be provided as a string.")    
        if len(species) > 11:
            raise Exception("Species names must be no longer than 11 characters. You provided '" + species + "', which is " + str(len(species)) + " characters.")
        self._species = species
        
    height = property(operator.attrgetter('_height'))
    
    @height.setter
    def height(self, height):
        # idk, I'll figure out how I want to store this later.
        if not height:
            raise Exception("Pokemon need a height.")
        self._height = int(height)
    
    weight = property(operator.attrgetter('_weight'))
    
    @weight.setter
    def weight(self, weight):
        # idk, I'll figure out how I want to store this later.
        if not weight:
            raise Exception("Pokemon need a weight.")
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
        if not icon_pals:
            raise Exception("Pokemon need icon palettes")
        self._icon_pals = icon_pals
    
    flavor_text = property(operator.attrgetter('_flavor_text'))
    
    @flavor_text.setter
    def flavor_text(self, flavor_text):
        if not flavor_text:
            raise Exception("Pokemon need flavor text.")
        # update later.
        self._flavor_text = flavor_text
        
    normal_palette = property(operator.attrgetter('_normal_palette'))
    
    @normal_palette.setter
    def normal_palette(self, normal_palette):
        if not normal_palette:
            raise Exception("Pokemon need a normal palette.")
        # update later
        self._normal_palette = normal_palette
        
    shiny_palette = property(operator.attrgetter('_shiny_palette'))
    
    @shiny_palette.setter
    def shiny_palette(self, shiny_palette):
        if not shiny_palette:
            raise Exception("Pokemon need a shiny palette.")
        # update later
        self._shiny_palette = shiny_palette
    
    def generate_yaml(self):
        level_ups =[]
        for move in self.level_up_moves:
            level_ups.append({int(move[0]) : move[1]})
        yml = {
            "constant": self.constant,
            "name": self.name,
            "types": self.types,
            "base-stats": {
                "hp": self.hp,
                "attack": self.attack,
                "defense": self.defense,
                "speed": self.speed,
                "special-attack": self.sp_attack,
                "special-defense": self.sp_defense
            },
            "growth-rate": self.growth_rate,
            "catch-rate": self.catch_rate,
            "base-experience": self.base_xp
        }
        if self.held_items:
            yml["held-items"] = self.held_items
        yml["female-ratio"] = self.gender_ratio
        yml["egg-cycle"] = self.egg_step_cycle
        yml["egg-groups"] = self.egg_groups
        yml["evolutions"] = self.evolutions
        yml["moves"] = {}
        yml["moves"]["level-up"] = level_ups
        yml["species"] = self.species
        yml["height"] = self.height
        yml["weight"] = self.weight
        yml["pokedex-entries"] = self.flavor_text
        yml["icon"] = self.icon
        yml["icon-palettes"] = self.icon_pals
        if self.taught_moves:
            yml["moves"]["taught"] = self.taught_moves
        if self.egg_moves:
            yml["moves"]["egg"] = self.egg_moves
        file_name = 'pokemon/' + self.constant.lower() + '.yml'
        with open(file_name, 'w') as file:
            documents = yaml.dump(yml, file, sort_keys=False)

class Pokedex:
    def __init__(self):
        self.pokemonList = []
    
    def addPokemon(self, pokemon):
        self.pokemonList.append(pokemon)

    def findPokemon(self, const):
        for obj in self.pokemonList:
            if obj.constant == const:
                return obj
        return False