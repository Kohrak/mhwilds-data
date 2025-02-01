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


MSG_FILES = [
        "wilds/combined_msgs.json"
]

def parse_skills(self):
    f = open(os.path.join(base, "natives/stm/gamedesign/common/equip/skilldata.user.3.json"))
    skilldata = next(iter(json.load(f).values()))["_Values"]
    f = open(os.path.join(base, "natives/stm/gamedesign/common/equip/skillcommondata.user.3.json"))
    skillcommondata = next(iter(json.load(f).values()))["_Values"]
    common = {}
    for skill in skillcommondata:
        id = skill["_skillId"]
        name = self.get_msg_by_guid(skill["_skillName"])
        explain = self.get_msg_by_guid(skill["_skillExplain"])
        icon = skill["_SkillIconType"]
        common[id] = {
                "name": name,
                "explain": explain,
                "category": skill["_skillCategory"],
                "type": skill["_skillType"],
                "icon": icon,
                "levels": {}
        }
        out_dir = "wilds/data/skill_icons"
        if id != "NONE" and icon != "INVALID":
            icon_idx = int(icon.replace("SKILL_", ""))
            tex_name = f"MHWilds-{SKILL_ICONS_WILDS[icon_idx]} Icon.png"
            icon_path = os.path.join(out_dir, tex_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            #if not os.path.exists(icon_path):
            icon_tex_base = COL_ICONS[icon_idx].copy()
            icon_tex_base.save(icon_path)

    results = {}
    for skill in skilldata:
        id = skill["_skillId"]
        name = self.get_msg_by_guid(skill["_skillName"])
        explain = self.get_msg_by_guid(skill["_skillExplain"])
        open_skills = [s for s in skill["_openSkill"] if s != "NONE"]
        lvl = skill["_SkillLv"]
        skill_lvl_data = {
                "id": id,
                "lvl": lvl,
                "name": name,
                "explain": explain,
                "open_skills": open_skills, # i dont actually know what this means, but i think its what can give the skill
                "data_values": skill["_value"],
        }
        
        if results.get(id) is None:
            results[id] = {}
        results[id][lvl] = skill_lvl_data
        #for open_skill in [s for s in skill["_openSkill"] if s != "NONE"]:
        if parent := common.get(id):
            parent["levels"][lvl] = skill_lvl_data

    return results, common

def parse_mealskills(self):
    f = open(os.path.join(base, "natives/stm/gamedesign/common/facility/mealskilldata.user.3.json"))
    skilldata = next(iter(json.load(f).values()))["_Values"]
    results = {}
    out_dir = "wilds/data/skill_icons"
    for skill in skilldata:
        id = skill["_MealSkill"]
        name = self.get_msg_by_guid(skill["_Name"])
        explain = self.get_msg_by_guid(skill["_Explain"])
        icon = skill["_SkillIcon"]
        if id != "NONE" and icon != "INVALID":
            icon_idx = int(icon.replace("SKILL_", ""))
            icon = SKILL_ICONS_WILDS[icon_idx]
            tex_name = f"MHWilds-{icon} Icon.png"
            icon_path = os.path.join(out_dir, tex_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            #if not os.path.exists(icon_path):
            icon_tex_base = COL_ICONS[icon_idx].copy()
            icon_tex_base.save(icon_path)
        results[id] = {
                "name": name,
                "explain": explain,
                "icon": icon,
        }
    return results


skills, skills_common = Parser2(parse_skills, MSG_FILES, base, msg_ext="").parse()
with open('wilds/data/skilldata.json', 'w') as f:
    json.dump(skills, f, ensure_ascii=False, indent=4)
with open('wilds/data/skillcommondata.json', 'w') as f:
    json.dump(skills_common, f, ensure_ascii=False, indent=4)

meal_skills = Parser2(parse_mealskills, MSG_FILES, base, msg_ext="").parse()
with open('wilds/data/mealskilldata.json', 'w') as f:
    json.dump(meal_skills, f, ensure_ascii=False, indent=4)
