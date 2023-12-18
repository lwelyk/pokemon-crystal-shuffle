import re

def check_constant(const, name="This Constant"):
    if bool(re.search(r'^\w*$', const)) is False:
        raise Exception(
            name + " can only have letters, numbers, and '_'s, failed with '" + 
            const + "'."
        )
    if const.upper() != const:
        print(
            "Converting constant to uppercase, please use uppercase for constants." +
            "Warned on '" + const + "'."
        )
        const = const.upper()
    return const

def check_number(val, min_no=0, max_no=255, name="This Value"):
    if type(val) != int:
        if val.isnumeric() is False:
            raise Exception(name + " must be a number.")
        val = int(val)
    if val > max_no or val < min_no:
        raise Exception(
            name + " must be higher than " + min_no + 
            " or lower than " + max_no + ", value was " + val)
    return val

def check_string(string, max_len, name="This String"):
    if len(string) > max_len:
        raise Exception(
            name + " can only be " + max_len + " characters. Failed with '" + 
            string + "'."
        )
    return string

def validate_type(p_type):
    # Temporarily just having a list here, will pull from types.yml later
    type_list = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]
    if type(p_type) != str:
        raise Exception("Types should be a string")
    if p_type not in type_list:
        raise Exception("Type " + p_type + " not found.")
    return p_type
