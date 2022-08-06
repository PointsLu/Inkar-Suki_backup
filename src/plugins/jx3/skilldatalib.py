from urllib.error import HTTPError
import nonebot
import sys
import os
import json
from nonebot.adapters.onebot.v11 import MessageSegment
from pathlib import Path
TOOLS = nonebot.get_driver().config.tools_path
sys.path.append(TOOLS)
ASSETS = TOOLS[:-5] + "assets"
from utils import get_url, get_status, nodetemp, get_content, get_api
from file import read, write
from config import Config

def aliases(SkillName: str) -> str:
    if SkillName in ["隐龙诀","隐龙决","隐龙","凌雪","凌雪阁"]:
        return "隐龙诀"
    elif SkillName in ["花间","花间游"]:
        return "花间游"
    elif SkillName in ["奶花","花奶","离经","离经易道"]:
        return "离经易道"
    elif SkillName in ["傲雪","傲血","傲血战意"]:
        return "傲血战意"
    elif SkillName in ["天策T","策T","铁牢","铁牢律"]:
        return "铁牢律"
    elif SkillName in ["气纯","紫霞功","紫霞"]:
        return "紫霞功"
    elif SkillName in ["剑纯","太虚剑意"]:
        return "太虚剑意"
    elif SkillName in ["奶秀","秀奶","云裳心经"]:
        return "云裳心经"
    elif SkillName in ["冰心","冰心诀"]:
        return "冰心诀"
    elif SkillName in ["毒经"]:
        return "毒经"
    elif SkillName in ["奶毒","毒奶","补天诀","补天决","补天"]:
        return "补天诀"
    elif SkillName in ["惊羽诀","惊羽决","鲸鱼","惊羽"]:
        return "惊羽诀"
    elif SkillName in ["天罗诡道","田螺","天罗"]:
        return "田螺"
    elif SkillName in ["问水诀","问水决","问水","轻剑"]:
        return "问水诀"
    elif SkillName in ["山居剑意","山居","重剑"]:
        return "山居剑意"
    elif SkillName in ["丐帮","笑尘决","笑尘决","笑尘"]:
        return "笑尘诀"
    elif SkillName in ["焚影圣诀","焚影圣决","焚影"]:
        return "焚影圣诀"
    elif SkillName in ["明教T","喵T","明尊","明尊琉璃体"]:
        return "明尊琉璃体"
    elif SkillName in ["苍云T","铁骨","铁骨衣"]:
        return "铁骨衣"
    elif SkillName in ["分山劲","分山"]:
        return "分山劲"
    elif SkillName in ["莫问"]:
        return "莫问"
    elif SkillName in ["奶歌","歌奶","相知"]:
        return "相知"
    if SkillName in ["北傲决","北傲诀","霸刀","北傲"]:
        return "北傲诀"
    elif SkillName in ["蓬莱","凌海","凌海诀"]:
        return "凌海诀"
    elif SkillName in ["洗髓经","洗髓","和尚T","秃T"]:
        return "洗髓经"
    elif SkillName in ["易筋经","易筋"]:
        return "易筋经"
    elif SkillName in ["衍天","衍天宗","太玄经","太玄"]:
        return "太玄经"
    elif SkillName in ["奶药","药奶","灵素"]:
        return "灵素"
    elif SkillName in ["无方"]:
        return "无方"
    else:
        return False

async def getSkills():
    '''
    获取所有门派的技能。
    
    数据来源：`JX3BOX` & `JX3API`。
    '''
    force_list = await get_api("https://raw.githubusercontent.com/JX3BOX/jx3box-data/master/data/xf/forceid.json")
    data_list = []
    for i in force_list:
        data_list.append(i)
    for i in data_list:
        if await get_status(url=f"https://data.jx3box.com/bps/v1/{i}/skill.json") != 404:
            info = await get_url(url = f"https://data.jx3box.com/bps/v1/{i}/skill.json")
            data = json.loads(info)
            for a in data["data"]:
                write(ASSETS + "/jx3/skills/" + a["kungfuName"] + ".json", json.dumps(a))

async def get_icon(skillName: str, api_icon: str = None) -> str:
    final_path = ASSETS + "/jx3/icons/" + skillName + ".png"
    if os.path.exists(final_path):
        return "[CQ:image,file=" + Path(final_path).as_uri() + "]"
    else:
        api_icon_url = api_icon
        try:
            icon = await get_content(api_icon_url)
        except:
            raise HTTPError(msg = "Can't connect to " + api_icon_url + ".")
        cache = open(ASSETS + "/jx3/icons/" + skillName + ".png", mode = "wb")
        cache.write(icon)
        cache.close()
        return "[CQ:image,file=" + Path(final_path).as_uri() + "]"

async def getAllSkillsInfo(Kungfu: str):
    '''
    获取心法下所有技能。
    '''
    Kungfu = aliases(Kungfu)
    if Kungfu == "隐龙诀":
        Kungfu == "隐龙决" # 由于`JX3Box`的`API`的数据错误问题，目前只能这样适配，等到数据纠正后删除这块代码。
    skill = read(ASSETS + "/jx3/skills/" + Kungfu + ".json")
    if skill == False:
        await getSkills()
        await getAllSkillsInfo(Kungfu)
    if Kungfu == False:
        return False
    skills = json.loads(skill)
    node = []
    moreInfo = skills["remarks"]
    for i in moreInfo:
        for x in i["forceSkills"]:
            image = await get_icon(x["skillName"], x["icon"]["FileName"])
            releaseType = x["releaseType"] # 释放类型
            if releaseType != "瞬间释放":
                releaseType = releaseType + "释放"
            if releaseType == "":
                releaseType = "释放时间未知"
            cd = x["cd"] # 调息时间
            skillName = x["skillName"] # 技能名
            specialDesc = x["specialDesc"] # 简单描述
            weapon = x["weapon"] # 武器
            desc = x["desc"] # 描述
            simpleDesc = x["simpleDesc"] # 简单描述，包含伤害/治疗/威胁值等基础信息
            distance = x["distance"] # 距离
            consumption = x["consumption"] # 内力消耗
            cheasts = x["cheasts"] # 秘籍
            skillType = i["remark"] # 武学派别
            if len(cheasts) == 0:
                cheastsInfo = "无"
            else:
                cheastsInfo = ""
                for y in cheasts:
                    cheastsInfo = cheastsInfo + "\n" + y["name"] + "\n" + y["desc"] + "\n"
            msg = image + f"\n技能名：{skillName}\n{releaseType} {cd}\n距离：{distance}\n武器：{weapon}\n内力消耗：{consumption}\n{specialDesc}\n{desc}\n{simpleDesc}\n技能归属：{skillType}\n秘籍：{cheastsInfo}"
            node.append(nodetemp(f"{Kungfu}技能", Config.bot[0], msg))
    return node