from data_handlers import pokemon_data, move_data, item_data, yaml_loaders
import yaml

test = pokemon_data.Pokedex()
test.load_pokedex_file("pokedex.csv")
test.create_pokemon_objects()
