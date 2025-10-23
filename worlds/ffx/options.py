"""
Option definitions for Final Fantasy ¨X
"""
from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, Option, Range, Toggle, PerGameCommonOptions

class GoalRequirement(Choice):
    """
    Sets the requirement to start the final battles. Defeating Yu Yevon is always the goal
    None: No requirements.
    Party Members: Requires unlocking all party members.
    Pilgrimage: Complete all the temples.
    """
    display_name = "Goal Requirement"
    default = 0
    option_none = 0
    option_party_members = 1
    option_pilgrimage = 2


class APMultiplier(Range):
    """
    Sets the AP multiplier.
    Default is 2.
    """
    display_name = "AP Multiplier"
    default = 2
    range_start = 1
    range_end = 10


class SphereGridRandomization(Choice):
    """
    Sets whether the Sphere Grid is randomized.
    Default is off.
    """
    display_name = "Sphere Grid Randomization"
    default = 0
    option_off = 0


class SuperBosses(Toggle):
    """
    Sets whether super boss locations are included or not. If off they will only have filler items.
    Default is off.
    """
    display_name = "Super Bosses"
    default = 0
    option_off = 0
    option_on = 1


class TrapsEnabled(Range):
    """
    Sets whether traps will be shuffled into the item pool.
    Default is 0.
    """
    display_name = "Traps Enabled"
    default = 0
    range_start = 0
    range_end = 100


class LogicDifficulty(Range):
    """
    Sets how strict the logic is for region access. Higher is harder/ less restrictive.
    Default is 3.
    """
    display_name = "Logic Difficulty"
    default = 3
    range_start = 1
    range_end = 10

@dataclass
class FFXOptions(PerGameCommonOptions):
    goal_requirement: GoalRequirement
    ap_multiplier: APMultiplier
    sphere_grid_randomization: SphereGridRandomization
    super_bosses: SuperBosses
    traps_enabled: TrapsEnabled
    logic_difficulty: LogicDifficulty
