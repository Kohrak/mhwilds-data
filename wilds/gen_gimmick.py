import os
import sys

from icon_map import *
from colors import *
from images import *
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from parser import Parser2
import json
import struct

BASE = os.environ["BASE"]

MSG_FILES = ["combined_msgs.json"]

def getpog():
    f = open(os.path.join(BASE, "natives/stm/gamedesign/stage/st101/layout/loaded/gimmick/pointgraph/st101_pointlist_gimmick.poglst.0.json"))
    poglist = json.load(f)["paths"]
    pog_ver = 10
    base = os.path.join(BASE, "natives/stm/")
    points = []
    names = []
    for pogpath in poglist:
        f = open(os.path.join(base, pogpath.lower()) + f".{pog_ver}.json")
        pog = json.load(f)
        if pog[0][0]["type"] != "app.point_graph_data.ContextLayoutGimmick":
            continue
        for val in pog[0]:
            point = val["rsz"]["v1"]
            gmid = val["rsz"]["_GmID"]
            #if "GM003" not in gmid:
            #    continue
            point = struct.unpack('<4f', bytes(point))
            points.append(point[0:3])
            names.append(gmid)
    return points, names


def parse_gimmicks(self):
    f = open(os.path.join(base, "natives/stm/gamedesign/common/gimmick/gimmicktextdata.user.3.json"))
    textdata = next(iter(json.load(f).values()))["_Values"]
    f = open(os.path.join(base, "natives/stm/gamedesign/common/gimmick/gimmickbasicdata.user.3.json"))
    basicdata = next(iter(json.load(f).values()))["_Values"]

    gimmicks = {}
    for gimmick in textdata:
        id = gimmick["_GimmickId"]
        name = self.get_msg_by_guid(gimmick["_Name"])
        expl = self.get_msg_by_guid(gimmick["_Explain"])
        gimmicks[id] = {
            "name": name,
            "explain": expl,
            "icon": "question mark",
            "color": "none",
            "map_icon": None,
            "points": [],
        }
    for gimmick in basicdata:
        id = gimmick["_GimmickId"]
        icon = gimmick["_IconType"]
        icon_idx = None
        tex_name = ""
        color = ""
        color_id = gimmick["_IconColor"]
        if "INVALID" not in icon:
            icon_idx = int(icon.strip("ITEM_"))
            icon = ICONS_WILDS[icon_idx]
            color = color_id.replace("I_", "").lower().capitalize()
            tex_name = f"MHWilds-{icon} Icon {color}.png"
        map_icon_id = gimmick["_MapIconType"]
        map_icon_idx = None
        if map_icon_id != "INVALID":
            map_icon_idx = int(map_icon_id.split("_")[-1]) + 16 * 20

        name = None
        explain = None
        if gim := gimmicks.get(id):
            name = gim["name"]
            explain = gim["explain"]
        gimmicks[id] = {
            "name": name,
            "explain": explain,
            "icon": icon,
            "color": color,
            "map_icon": gimmick["_MapIconType"],
            "points": [],
        }

        out_dir = "wilds/data/gimmick_icons"
        icon_path = os.path.join(out_dir, tex_name)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        #if not os.path.exists(icon_path):
        if icon_idx is not None:
            icon_tex_base = ICONS_TEX[icon_idx].copy()
            color = COLORS[WILDS_COLOR_IDX_MAP[color_id]]
            icon_tex = multiply_image_by_color(icon_tex_base, color[:3])
            icon_tex.save(icon_path)

        if map_icon_idx is not None:
            map_tex_name = f"MHWilds-{id} Map Icon.png"
            map_icon_path = os.path.join(out_dir, map_tex_name)
            color = COLORS[WILDS_COLOR_IDX_MAP[color_id]]
            map_tex = ICONS_TEX[map_icon_idx].copy()
            map_tex = multiply_image_by_color(map_tex, color[:3])
            map_tex.save(map_icon_path)

    points, names = getpog()
    for point, name in zip(points, names):
        if gimmicks.get(name):
            gimmicks[name]["points"].append(point)
        else:
            gimmicks[name] = {
                "name": None,
                "explain": None,
                "icon": "Question Qark",
                "color": "None",
                "map_icon": None,
                "points": [],
            }
    return gimmicks

gimmick_data = Parser2(parse_gimmicks, MSG_FILES, base, msg_ext="").parse()
with open('wilds/data/gimmickdata.json', 'w') as f:
    json.dump(gimmick_data, f, ensure_ascii=False, indent=4)

