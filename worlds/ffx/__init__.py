"""
Archipelago World definition for Final Fantasy X
"""

from typing import ClassVar, Any, Optional
from random import Random
import settings

from BaseClasses import Tutorial, Item, ItemClassification
from worlds.AutoWorld import WebWorld, World
from Utils import visualize_regions

from .client import FFXClient

from .items import create_item_label_to_code_map, item_table, key_items, filler_items, AllItems, FFXItem, party_member_items, stat_abilities, skill_abilities, region_unlock_items, trap_items
from .locations import create_location_label_to_id_map, FFXLocation
from .regions import create_regions
from .options import FFXOptions
from .generate import generate_output


class FFXWebWorld(WebWorld):
    """
    Webhost info for Final Fantasy X
    """
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy X with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Rurusachi"]
    )

    tutorials = [setup_en]


class FFXSettings(settings.Group):
    pass


class FFXWorld(World):
    """
    Final Fantasy X is a game
    """
    game = "Final Fantasy X"
    web = FFXWebWorld()
    topology_present = False

    settings_key = "ffx_options"
    settings: ClassVar[FFXSettings]

    options_dataclass = FFXOptions
    options: FFXOptions

    required_client_version = (0, 4, 4)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()

    def get_filler_item_name(self) -> str:
        filler = [x.itemName for x in filler_items]
        return self.random.choice(filler)

    def create_regions(self) -> None:
        create_regions(self, self.player)

    def create_items(self):

        required_items = []

        for item in key_items:
            required_items.append(item.itemName)

        # for item in skill_abilities:
        #     required_items.append(item.itemName)
        #
        # for item in stat_abilities:
        #     required_items.extend([item.itemName for _ in range(1)])

        #self.random.shuffle(region_unlock_items)
        starting_region = self.random.choice(region_unlock_items[:min(self.options.logic_difficulty.value, 3)]) # Baaj, Besaid, or Kilika
        #starting_region = region_unlock_items[0]

        self.multiworld.push_precollected(self.create_item(starting_region.itemName))
        for item in region_unlock_items:
            if item != starting_region:
                required_items.append(item.itemName)

        starting_character = party_member_items[0]

        self.multiworld.push_precollected(self.create_item(starting_character.itemName))
        for party_member in party_member_items:
            if party_member == starting_character:
                continue
            required_items.append(party_member.itemName)

        unfilled_locations = len(self.multiworld.get_unfilled_locations(self.player))

        items_remaining = unfilled_locations - len(required_items)

        for itemName in required_items:
            self.multiworld.itempool.append(self.create_item(itemName))

        useful_items = []
        for item in AllItems:
            if item.progression == ItemClassification.useful:
                useful_items += [item.itemName]

        self.random.shuffle(useful_items)

        if self.options.traps_enabled.value > 0:
            useful_items = [trap_items[0].itemName for _ in range(self.options.traps_enabled.value)] + useful_items

        for i in range(items_remaining):
            if i > len(useful_items) - 1:
                self.multiworld.itempool.append(self.create_filler())
            else:
                self.multiworld.itempool.append(self.create_item(useful_items[i]))

    def create_item(self, name: str) -> Item:
        item = item_table[name]
        return FFXItem(item.itemName, item.progression, item.itemID, self.player)

    def generate_basic(self) -> None:
        victory_event = FFXItem('Victory', ItemClassification.progression, None, self.player)

        final_aeon = self.get_location("Sin: Braska's Final Aeon")

        final_aeon.place_locked_item(victory_event)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        match self.options.goal_requirement.value:
            case self.options.goal_requirement.option_none:
                pass
            case self.options.goal_requirement.option_party_members:
                final_aeon.access_rule = lambda state: state.has_all(
                    [character.itemName for character in party_member_items], self.player)
            case self.options.goal_requirement.option_pilgrimage:
                pilgrimage_events = {
                    "S.S. Liki 1st visit": "Pilgrimage: Besaid",
                    "S.S. Winno 1st visit": "Pilgrimage: Kilika",
                    "Djose 1st visit": "Pilgrimage: Djose",
                    "Lake Macalania 1st visit: Post-Wendigo": "Pilgrimage: Macalania",
                    "Bevelle 1st visit: Post-Seymour Natus": "Pilgrimage: Bevelle",
                    "Zanarkand Ruins 1st visit: Post-Yunalesca": "Pilgrimage: Zanarkand Ruins",
                }
                for region_name, location_name in pilgrimage_events.items():
                    self.get_region(region_name).add_event(location_name, location_type=FFXLocation, item_type=FFXItem)

                final_aeon.access_rule = lambda state: state.has_all(list(pilgrimage_events.values()))


    def generate_output(self, output_directory: str) -> None:

        # Visualize regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), f"ffx {self.player}.puml", show_entrance_names=True)

        generate_output(self, self.player, output_directory)