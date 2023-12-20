import operator
import re
import yaml
from . import common

class Item:
    def __init__(
        self,
        constant,
        name,
        price,
        held_effect,
        parameter,
        item_property,
        pocket,
        field_menu,
        battle_menu,
        description,
        effect
    ):
        self.constant = constant
        self.name = name
        self.price = price
        self.held_effect = held_effect
        self.parameter = parameter
        self.item_property = item_property
        self.pocket = pocket
        self.field_menu = field_menu
        self.battle_menu = battle_menu
        self.description = description
        self.effect = effect

    constant = property(operator.attrgetter('_constant'))
    
    @constant.setter
    def constant(self, const):
        if not const: 
            raise Exception ("Items need a constant.")
        self._constant = common.check_constant(const)

    name = property(operator.attrgetter('_name'))
    
    @name.setter
    def name(self, name):
        if not name:
            raise Exception("Items need a name.")
        self._name = common.check_string(name, 12, "Item Names")
        
    price = property(operator.attrgetter('_price'))
    
    @price.setter
    def price(self, price=0):
        if not price:
            raise Exception("Pokemon need a price.")
        if price == "$9999":
            self._price = price
        else:
            self._price = common.check_number(price, 0, 65535, "Price")
        
    held_effect = property(operator.attrgetter('_held_effect'))
    
    @held_effect.setter
    def held_effect(self, held_effect):
        # Add something to make sure the effect exists later.
        self._held_effect = held_effect
    
    parameter = property(operator.attrgetter('_parameter'))
    
    @parameter.setter
    def parameter(self, parameter=0):
        self._parameter = common.check_number(parameter, -1, 255, "Item Parameter")
    
    item_property = property(operator.attrgetter('_item_property'))
    
    @item_property.setter
    def item_property(self, item_property="CANT_SELECT"):
        self._item_property = item_property
        
    pocket = property(operator.attrgetter('_pocket'))
    
    @pocket.setter
    def pocket(self, pocket):
        # Add something to make sure the pocket is real later.
        self._pocket = pocket

    field_menu = property(operator.attrgetter('_field_menu'))
    
    @field_menu.setter
    def field_menu(self, field_menu="ITEMMENU_NOUSE"):
        # Add something to make sure the field_menu is real later.
        self._field_menu = field_menu

    battle_menu = property(operator.attrgetter('_battle_menu'))

    @battle_menu.setter
    def battle_menu(self, battle_menu="ITEMMENU_NOUSE"):
        # Add something to make sure the battle_menu is real later.
        self._battle_menu = battle_menu

    description = property(operator.attrgetter('_description'))

    @description.setter
    def description(self, description):
        if not description:
            raise Exception("Items need Descriptions.")
        # update later.
        self._description = description

    effect = property(operator.attrgetter('_effect'))

    @effect.setter
    def effect(self, effect="NoEffect"):
        # Add something to make sure the effect is real later.
        self._effect = effect
 
    def generate_yaml(self):
        yml = {
            "constant": self.constant,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "pocket": self.pocket,
            "held-effect": self.held_effect,
            "parameter": self.parameter,
            "effect": self.effect,
            "item-property": self.item_property,
            "field-menu": self.field_menu,
            "battle-menu": self.battle_menu,
        }
        file_name = 'items/' + self.constant.lower() + '.yml'
        with open(file_name, 'w') as file:
            documents = yaml.dump(yml, file, sort_keys=False)
