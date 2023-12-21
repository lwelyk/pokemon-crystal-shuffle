from data_handlers import pokemon_data, move_data, item_data, yaml_loaders
import yaml

test = pokemon_data.Pokedex()
test.loadPokedexFile("pokedex.csv")
test.createPokemonObjects()
