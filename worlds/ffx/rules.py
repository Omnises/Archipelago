import typing
from collections import Counter
from typing import Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, CollectionRule
from .items import character_names, stat_abilities, item_to_stat_value
if typing.TYPE_CHECKING:
    from .__init__ import FFXWorld
else:
    FFXWorld = object

world_battle_levels: dict[str, int] = {
"Baaj Temple":                 1,
"Besaid":                      2,
"Kilika":                      3,
"Luca":                        4,
"Mi'ihen Highroad":            5,
"Mushroom Rock Road":          6,
"Djose":                       7,
"Moonflow":                    8,
"Guadosalam":                  9,
"Thunder Plains":             10,
"Macalania":                  11,
"Bikanel":                    12,
"Bevelle":                    13,
"Calm Lands":                 14,
"Cavern of the Stolen Fayth": 14,
"Mt. Gagazet":                15,
"Zanarkand Ruins":            16,
"Sin":                        17,
"Airship":                    13,
"Omega Ruins":                18,
}

region_to_first_visit: dict[str, str] = {
"Baaj Temple":                "Baaj Temple 1st visit",
"Besaid":                     "Besaid Island 1st visit",
"Kilika":                     "Kilika 1st visit: Pre-Geneaux",
"Luca":                       "Luca 1st visit: Pre-Oblitzerator",
"Mi'ihen Highroad":           "Mi'ihen Highroad 1st visit: Pre-Chocobo Eater",
"Mushroom Rock Road":         "Mushroom Rock Road 1st visit: Pre-Sinspawn Gui",
"Djose":                      "Djose 1st visit",
"Moonflow":                   "Moonflow 1st visit: Pre-Extractor",
"Guadosalam":                 "Guadosalam 1st visit",
"Thunder Plains":             "Thunder Plains 1st visit",
"Macalania":                  "Macalania Woods 1st visit: Pre-Spherimorph",
"Bikanel":                    "Bikanel 1st visit",
"Bevelle":                    "Bevelle 1st visit: Pre-Isaaru",
"Calm Lands":                 "Calm Lands 1st visit: Pre-Defender X",
"Cavern of the Stolen Fayth": "Cavern of the Stolen Fayth 1st visit",
"Mt. Gagazet":                "Mt. Gagazet 1st visit: Pre-Biran and Yenke",
"Zanarkand Ruins":            "Zanarkand Ruins 1st visit: Pre-Spectral Keeper",
"Sin":                        "Sin: Pre-Seymour Omnis",
"Airship":                    "Airship 1st visit: Pre-Evrae",
"Omega Ruins":                "Omega Ruins: Pre-Ultima Weapon",
}




def create_region_access_rule(world: FFXWorld, region_name: str):
    region_level = world_battle_levels[region_name]
    if region_level < 5:
        return lambda state: state.has(f"Region: {region_name}", world.player)
    else:
        appropriate_level_regions = [other_region for other_region, other_level in world_battle_levels.items() if
                                     other_region != region_name and region_level > other_level >= region_level - world.options.logic_difficulty.value]

        return lambda state: state.has(f"Region: {region_name}", world.player) and any([state.can_reach_region(region_to_first_visit[other_region], world.player) for other_region in appropriate_level_regions])

def create_level_rule(world: FFXWorld, level: int):
    appropriate_level_regions = [other_region for other_region, other_level in world_battle_levels.items() if
                                 level > other_level >= level - world.options.logic_difficulty.value]

    return lambda state: any([state.can_reach_region(region_to_first_visit[other_region], world.player) for other_region in appropriate_level_regions])

def create_ability_rule(world: FFXWorld, ability_name: str):
    #return lambda state: state.has_any([f"{name} Ability: {ability_name}" for name in character_names], world.player)
    #return lambda state: True;               "       Ability: Fire"
    #temp = [(f"{name} Ability: {ability_name}", f"Party Member: {name}") for name in character_names]
    #for ability, character in temp:
    #    print(world.item_name_to_id[ability])
    #    print(world.item_name_to_id[character])
    #print(temp)
    if world.options.sphere_grid_randomization.value == world.options.sphere_grid_randomization.option_on:
        return lambda state: any([state.has_all([f"{name} Ability: {ability_name}", f"Party Member: {name}"], world.player) for name in character_names])
    else:
        return lambda state: True


#def create_stat_rule(world: World, stat_total: int):
#    return lambda state: state.has
def create_stat_total_rule(world: FFXWorld, num_party_members: int, stat_total: int) -> CollectionRule:
    def has_stat_total(state: CollectionState) -> bool:
        player_prog_items = state.prog_items[world.player]
        totals = Counter()
        for item, count in player_prog_items.items():
            if item in stat_abilities:
                character, value = item_to_stat_value[item]
                totals[character] += value*count

        return len([total for total in totals.values() if total > stat_total]) >= num_party_members
        #for total in totals.values():
        #    if total > stat_total:
        #        return True
        #return False
    return has_stat_total

ruleDict: dict[str, Callable[[FFXWorld], CollectionRule]] = {
    "Sinspawn Geneaux":    lambda world: create_level_rule(world, 3),
    "Oblitzerator":        lambda world: create_level_rule(world, 4),
    "Chocobo Eater":       lambda world: create_level_rule(world, 5),
    "Sinspawn Gui":        lambda world: create_level_rule(world, 6),
    "Extractor":           lambda world: create_level_rule(world, 8),
    "Spherimorph":         lambda world: create_level_rule(world, 11),
    "Crawler":             lambda world: create_level_rule(world, 11),
    "Seymour/Anima":       lambda world: create_level_rule(world, 11),
    "Wendigo":             lambda world: create_level_rule(world, 11),
    "Evrae":               lambda world: create_level_rule(world, 13),
    "Airship Sin":         lambda world: create_level_rule(world, 16),
    "Overdrive Sin":       lambda world: create_level_rule(world, 16),
    "Penance":             lambda world: create_level_rule(world, 18),
    "Isaaru":              lambda world: create_level_rule(world, 13),
    "Evrae Altana":        lambda world: create_level_rule(world, 13),
    "Seymour Natus":       lambda world: create_level_rule(world, 13),
    "Defender X":          lambda world: create_level_rule(world, 14),
    "Biran and Yenke":     lambda world: create_level_rule(world, 15),
    "Seymour Flux":        lambda world: create_level_rule(world, 15),
    "Sanctuary Keeper":    lambda world: create_level_rule(world, 15),
    "Spectral Keeper":     lambda world: create_level_rule(world, 16),
    "Yunalesca":           lambda world: create_level_rule(world, 16),
    "Seymour Omnis":       lambda world: create_level_rule(world, 17),
    "Braska's Final Aeon": lambda world: create_level_rule(world, 17),
    "Ultima Weapon":       lambda world: create_level_rule(world, 18),
    "Omega Weapon":        lambda world: create_level_rule(world, 19),
    "Geosgaeno":           lambda world: create_level_rule(world, 16),

    "Baaj Temple":                lambda world: create_region_access_rule(world, "Baaj Temple"), # lambda state: state.has("Region: Baaj Temple", world.player),
    "Besaid":                     lambda world: create_region_access_rule(world, "Besaid"),
    "Kilika":                     lambda world: create_region_access_rule(world, "Kilika"),
    "Luca":                       lambda world: create_region_access_rule(world, "Luca"),
    "Mi'ihen Highroad":           lambda world: create_region_access_rule(world, "Mi'ihen Highroad"),
    "Mushroom Rock Road":         lambda world: create_region_access_rule(world, "Mushroom Rock Road"),
    "Djose":                      lambda world: create_region_access_rule(world, "Djose"),
    "Moonflow":                   lambda world: create_region_access_rule(world, "Moonflow"),
    "Guadosalam":                 lambda world: create_region_access_rule(world, "Guadosalam"),
    "Thunder Plains":             lambda world: create_region_access_rule(world, "Thunder Plains"),
    "Macalania":                  lambda world: create_region_access_rule(world, "Macalania"),
    "Bikanel":                    lambda world: create_region_access_rule(world, "Bikanel"),
    "Bevelle":                    lambda world: create_region_access_rule(world, "Bevelle"),
    "Calm Lands":                 lambda world: create_region_access_rule(world, "Calm Lands"),
    "Cavern of the Stolen Fayth": lambda world: create_region_access_rule(world, "Cavern of the Stolen Fayth"),
    "Mt. Gagazet":                lambda world: create_region_access_rule(world, "Mt. Gagazet"),
    "Zanarkand Ruins":            lambda world: create_region_access_rule(world, "Zanarkand Ruins"),
    "Sin":                        lambda world: create_region_access_rule(world, "Sin"),
    "Airship":                    lambda world: create_region_access_rule(world, "Airship"),
    "Omega Ruins":                lambda world: create_region_access_rule(world, "Omega Ruins"),
}


def set_rules(world: FFXWorld, player) -> None:
    pass
    #add_rule(world.multiworld.get_region("Kilika 1st visit: Post-Geneaux", player).entrances[0], ruleDict["Sinspawn Geneaux"](world))
