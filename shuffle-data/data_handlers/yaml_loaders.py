import yaml
import os
from . import pokemon_data, item_data, move_data

class YLoader:
    
    def load_yaml(self, yml):
        if not os.path.exists(yml):
            raise Exception("Cannot find file " + str(yml))
        data = {}
        with open(yml, "r") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
        return data

    def poke_from_yml(self, constant):
        poke_dir = "pokemon/" # temp hardcode
        yml = poke_dir + str(constant).lower() + ".yml"
        if not os.path.exists(yml):
            raise Exception(
                "Pokemon data missing for " + str(constant) + "in " + str(poke_dir)
            )
        data = self.load_yaml(yml)
        if data:
            data["level_up_moves"] = []
            for move in data["moves"]["level_up"]:
                for lv, mv in move.items():
                    data["level_up_moves"].append((lv, mv))
            data["taught_moves"] = []
            if "taught_moves" in data["moves"]:
                data["taught_moves"] = data["moves"]["taught_moves"]
            data["egg_moves"] = []
            if "egg_moves" in data["moves"]:
                data["egg_moves"] = data["moves"]["egg_moves"]
            del data["moves"]
            if "held_items" not in data:
                data["held_items"] = []
            if "evolutions" not in data:
                data["evolutions"] = []

            return pokemon_data.Pokemon(**data)
        