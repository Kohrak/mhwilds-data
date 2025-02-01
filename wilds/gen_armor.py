
import os
import sys

from icon_map import *
from colors import *
from images import *
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from parser import Parser2
import json


base = os.environ["BASE"]

ITEM_MSG_FILES = ["wilds/combined_msgs.json"]

def parse_armor(self):
    f = open(os.path.join(base, "natives/stm/gamedesign/common/"))
    #itemdata = next(iter(json.load(f).values()))["_Values"]
    armor = {}
    return armor

#item_recipes = Parser2(parse_item_recipes, [], base, msg_ext=".23.json").parse(item_data)
#with open('wilds/data/itemrecipe.json', 'w') as f:
#    json.dump(item_recipes, f, ensure_ascii=False, indent=4)

