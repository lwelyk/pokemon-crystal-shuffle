import operator
import re
import yaml
from . import common

# Be a file or something later, just here for testing and setup
flags = {
    "SpecialStat": False,
    "PhysicalSpecialSplit": True
}

class Move:
    def __init__(
        self,
        constant,
        name,
        animation,
        effect,
        power,
        move_type,
        category,
        accuracy,
        pp,
        effect_chance,
        description
    ):
        self.constant = constant
        self.name = name
        self.animation = animation
        self.effect = effect
        self.power = power
        self.move_type = move_type
        self.category = category
        self.accuracy = accuracy
        self.pp = pp
        self.effect_chance = effect_chance
        self.description = description
        
    constant = property(operator.attrgetter('_constant'))
    
    @constant.setter
    def constant(self, const):
        if not const: 
            raise Exception ("Moves need a constant.")
        self._constant = common.check_constant(const, "Move")
        
    name = property(operator.attrgetter('_name'))
    
    @name.setter
    def name(self, name):
        if not name:
            raise Exception("Moves need a name.")
        self._name = common.check_string(name, 12, "Move Name")
    
    animation = property(operator.attrgetter('_animation'))
    
    @animation.setter
    def animation(self, animation):
        # Add checks later once animation objects exist.
        self._animation = animation
    
    effect = property(operator.attrgetter('_effect'))
    
    @effect.setter
    def effect(self, effect):
        # Add checks later once move_effect objects exist.
        self._effect = effect

    power = property(operator.attrgetter('_power'))
    
    @power.setter
    def power(self, power):
        if not power:
            raise Exception("Moves need Power")
        self._power = common.check_number(
            val=power, min_no=0, max_no=255, name="Power"
        )

    move_type = property(operator.attrgetter('_move_type'))
    
    @move_type.setter
    def move_type(self, move_type):
        if not move_type:
            raise Exception("Moves Need a type.")
        self._move_type = common.validate_type(move_type)

    category = property(operator.attrgetter('_category'))
    
    @category.setter
    def category(self, category=False):
        # Temporarily have this array here
        cat_list = ['Physical', 'Special', 'Status']  
        category = category.title()
        if flags["PhysicalSpecialSplit"]:
            if type(category) != str:
                raise Exception("Move categories should be a string")
            if category not in cat_list:
                raise Exception("Move Category " + category + " not found.")
            self._category = category
        else:
            # Temporarily live here
            type_cats = {
                "Normal": "Physical", 
                "Fighting": "Physical", 
                "Flying": "Physical", 
                "Poison": "Physical", 
                "Ground": "Physical", 
                "Rock": "Physical", 
                "Bug": "Physical", 
                "Ghost": "Physical", 
                "Steel": "Physical", 
                "Fire": "Special", 
                "Water": "Special", 
                "Grass": "Special", 
                "Electric": "Special", 
                "Psychic": "Special", 
                "Ice": "Special", 
                "Dragon": "Special", 
                "Dark": "Special", 
                "Fairy": "Special"
            }
            if self.type:
                if self.type in type_cats:
                    self._category = type_cats[self.type]
            elif category:
                if category in type_cats:
                    self._category = type_cats[category]
            else:
                raise Exception("When there is no physical special split, please set the move type first or Pass a type to this function.")

    accuracy = property(operator.attrgetter('_accuracy'))
    
    @accuracy.setter
    def accuracy(self, accuracy):
        if not accuracy:
            raise Exception("Moves need Accuracy")
        self._accuracy = common.check_number(
            val=accuracy, min_no=0, max_no=255, name="Accuracy"
        )

    pp = property(operator.attrgetter('_pp'))
    
    @pp.setter
    def pp(self, pp):
        # This just lives here for now
        max_pp = 40
        if not pp:
            raise Exception("Moves need PP")
        self._pp = common.check_number(
            val=pp, min_no=0, max_no=max_pp, name="PP"
        )

    effect_chance = property(operator.attrgetter('_effect_chance'))
    
    @effect_chance.setter
    def effect_chance(self, effect_chance=0):
        if not effect_chance:
            raise Exception("Moves need an Effect Chance")
        self._effect_chance = common.check_number(
            val=effect_chance, min_no=0, max_no=255, name="Effect Chance"
        )
        
    description = property(operator.attrgetter('_description'))
    
    @description.setter
    def description(self,  description):
        # Each move description has two lines with up to 18 characters each.
        # I'll figure out validation for this later.
        if not description:
            raise Exception("Moves need descriptions")
        self._description = description
    
    def generate_yaml(self):
        yml = {
            "constant": self.constant,
            "name": self.name,
            "type": self.move_type,
            "category": self.category,
            "description": self.description,
            "power": self.power,
            "accuracy": self.accuracy,
            "effect": self.effect,
            "effect-chance": self.effect_chance,
            "pp": self.pp,
            "animation": self.animation,
        }
        file_name = 'moves/' + self.constant.lower() + '.yml'
        with open(file_name, 'w') as file:
            documents = yaml.dump(yml, file, sort_keys=False)
