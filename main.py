from dataclasses import dataclass, field
import dataclasses
import json
import os
import random
import time
from typing import List, Dict, Tuple, Optional, Any

# ======================【配置文件区】======================
GAME_CONFIG = {
    "REALM_LIST": [
        {"name": "凡人", "exp_need": 0, "hp_add": 100, "zy_add": 50},
        {"name": "练气一层", "exp_need": 1000, "hp_add": 150, "zy_add": 80},
        {"name": "练气二层", "exp_need": 2500, "hp_add": 180, "zy_add": 100},
        {"name": "练气三层", "exp_need": 5000, "hp_add": 220, "zy_add": 130},
        {"name": "练气四层", "exp_need": 8000, "hp_add": 280, "zy_add": 180},
        {"name": "筑基初期", "exp_need": 12000, "hp_add": 400, "zy_add": 250},
        {"name": "筑基中期", "exp_need": 20000, "hp_add": 550, "zy_add": 350},
        {"name": "筑基后期", "exp_need": 28000, "hp_add": 700, "zy_add": 450},
        {"name": "金丹初期", "exp_need": 40000, "hp_add": 800, "zy_add": 500},
        {"name": "金丹中期", "exp_need": 60000, "hp_add": 1000, "zy_add": 650},
        {"name": "金丹后期", "exp_need": 85000, "hp_add": 1300, "zy_add": 800},
        {"name": "元婴", "exp_need": 130000, "hp_add": 1800, "zy_add": 1200},
        {"name": "化神", "exp_need": 220000, "hp_add": 2500, "zy_add": 1800},
    ],
    "SECT_POS": ["外门弟子", "内门弟子", "亲传弟子", "长老", "宗主"],
    "OFFLINE_RATE": 1.0,
    "CULTIVATE_CFG":{
        "normal_zy_cost":80,
        "normal_exp_gain":1200,
        "deep_stone_high_cost":3,
        "deep_exp_gain":4500
    },
    "ENEMY_LIB": [
        {"ename":"一阶野狼","pow_rate":0.6,"hp_rate":8,"drop":["妖兽兽核×1","灵草×1"]},
        {"ename":"二阶赤焰虎","pow_rate":1.0,"hp_rate":10,"drop":["妖兽兽核×2","聚气丹×1"]},
        {"ename":"三阶玄水巨蟒","pow_rate":1.4,"hp_rate":12,"drop":["妖兽兽核×3","破境丹×1","上品灵石袋"]},
        {"ename":"四阶金甲魔猿","pow_rate":1.8,"hp_rate":15,"drop":["妖兽兽核×5","宝器碎片"]},
        {"ename":"五阶荒古凶兽","pow_rate":2.4,"hp_rate":20,"drop":["妖兽兽核×8","神材碎片","洗髓丹×2"]},
    ],
    "SHOP_GOODS":[
        {"g_name":"淬体丹","g_cat":"丹药","g_num":1,"cost_low":300,"cost_high":0},
        {"g_name":"聚气丹","g_cat":"丹药","g_num":1,"cost_low":500,"cost_high":0},
        {"g_name":"固元丹","g_cat":"丹药","g_num":1,"cost_low":800,"cost_high":0},
        {"g_name":"破境丹","g_cat":"丹药","g_num":1,"cost_low":0,"cost_high":15},
        {"g_name":"洗髓丹","g_cat":"丹药","g_num":1,"cost_low":0,"cost_high":22},
        {"g_name":"速元丹","g_cat":"丹药","g_num":1,"cost_low":650,"cost_high":0},
        {"g_name":"灵能步枪蓝图","g_cat":"蓝图","g_num":1,"cost_low":0,"cost_high":25},
        {"g_name":"军阵罗盘蓝图","g_cat":"蓝图","g_num":1,"cost_low":0,"cost_high":30},
    ],
    "TERRITORY_CFG":[
        {"lv":1,"name":"边陲小邑","arm_max":200,"cost_low":0,"cost_high":0},
        {"lv":2,"name":"边塞重镇","arm_max":800,"cost_low":12000,"cost_high":40},
        {"lv":3,"name":"郡城","arm_max":2500,"cost_low":40000,"cost_high":120},
        {"lv":4,"name":"王都","arm_max":8000,"cost_low":120000,"cost_high":350},
    ],
    "ARRAY_LIB":[
        {"aname":"万灵基础军阵","pow_bonus":0.30,"cost_high":20},
        {"aname":"玄甲固防军阵","pow_bonus":0.45,"cost_high":45},
        {"aname":"雷霆杀伐军阵","pow_bonus":0.65,"cost_high":80},
    ],
    "FORGE_RECIPE":[
        {"r_name":"精铁战枪","slot":"武器","atk":120,"def":20,"need":{"宝器碎片":2,"妖兽兽核":10}},
        {"r_name":"玄灵法袍","slot":"防具","atk":40,"def":100,"need":{"宝器碎片":3,"灵草":15}},
    ],
    "ALCHEMY_RECIPE":[
        {"p_name":"淬体丹","need":{"灵草":8,"妖兽兽核":2}},
        {"p_name":"聚气丹","need":{"灵草":12,"妖兽兽核":3}},
        {"p_name":"洗髓丹","need":{"灵草":25,"妖兽兽核":8,"神材碎片":1}},
    ],
    "CITY_EVENT":[
        {"title":"流民归附","desc":"大批流民前来投奔大秦，军队上限小幅提升","effect":{"arm_add_max":100}},
        {"title":"灵矿开采","desc":"矿场产出灵石","effect":{"stone_low":2500,"stone_high":8}},
        {"title":"妖兽袭城","desc":"妖兽进攻城镇，消耗部分军队，战胜获得战利品","effect":{"arm_loss_rate":0.12}},
        {"title":"仙师到访","desc":"过路仙师指点，直接获得修为","effect":{"exp":6000}},
        {"title":"天灾歉收","desc":"灾年消耗国库资源","effect":{"stone_low":-1800}},
    ]
}

# ====================== 数据结构 ======================
@dataclass
class BuffDebuff:
    name: str
    desc: str
    type: str
    duration: int
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EquipItem:
    name: str
    rank: str
    slot: str
    atk_bonus: int = 0
    def_bonus: int = 0
    special: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BagItem:
    name: str
    category: str
    num: int
    desc: str = ""

@dataclass
class Player:
    name: str = "修士"
    realm_idx: int = 0
    exp: int = 0
    physique: int = 10
    hp: int = 100
    max_hp: int = 100
    zy: int = 50
    max_zy: int = 50
    patk: int = 20
    matk: int = 20
    crit_rate: float = 0.05
    crit_mult: float = 2.0
    break_def: float = 0.03
    dodge_rate: float = 0.02
    tough_dmg_reduce: float = 0.0
    stone_low: int = 500
    stone_high: int = 20
    nation_luck: int = 0
    territory_lv: int = 1
    army_count: int = 0
    army_arrays: List[Dict] = field(default_factory=list)
    sect_pos_idx: int = 0
    equip_slot: Dict[str, Optional[EquipItem]] = field(default_factory=dict)
    bag: List[BagItem] = field(default_factory=list)
    buffs: List[BuffDebuff] = field(default_factory=list)
    debuffs: List[BuffDebuff] = field(default_factory=list)
    total_power: float = 0.0
    enemy_book: List[str] = field(default_factory=list)
    last_offline_timestamp: float = field(default_factory=time.time)

# ====================== 工具类 ======================
class GameUtil:
    @staticmethod
    def get_debuff_mod(p: Player) -> float:
        mod = 1.0
        for db in p.debuffs:
            if "all_down" in db.params:
                mod *= (1.0 - db.params["all_down"])
        return mod

    @staticmethod
    def calc_total_power(p: Player) -> float:
        debuff_mod = GameUtil.get_debuff_mod(p)
        base = (p.physique * 2 + p.patk + p.matk + p.max_hp * 0.2) * debuff_mod
        mult = 1.0
        for b in p.buffs:
            if "power_mult" in b.params:
                mult *= b.params["power_mult"]
        territory_info = GAME_CONFIG["TERRITORY_CFG"][min(p.territory_lv-1, len(GAME_CONFIG["TERRITORY_CFG"])-1)]
        arm_max = territory_info["arm_max"]
        arm_eff = min(p.army_count, arm_max)
        arm_bonus = arm_eff * 0.06
        total = (base + arm_bonus) * mult
        return round(total, 2)

    @staticmethod
    def get_realm_name(p: Player) -> str:
        return GAME_CONFIG["REALM_LIST"][p.realm_idx]["name"]

    @staticmethod
    def get_territory_name(p: Player) -> str:
        idx = min(p.territory_lv-1, len(GAME_CONFIG["TERRITORY_CFG"])-1)
        return GAME_CONFIG["TERRITORY_CFG"][idx]["name"]

    @staticmethod
    def get_arm_max(p: Player) -> int:
        idx = min(p.territory_lv-1, len(GAME_CONFIG["TERRITORY_CFG"])-1)
        return GAME_CONFIG["TERRITORY_CFG"][idx]["arm_max"]

    @staticmethod
    def calc_offline_gain(p: Player) -> Tuple[int, int]:
        now = time.time()
        delta_sec = int(now - p.last_offline_timestamp)
        p.last_offline_timestamp = now
        exp_gain = int(delta_sec * 0.8 * GAME_CONFIG["OFFLINE_RATE"])
        stone_gain = int(delta_sec * 0.2 * GAME_CONFIG["OFFLINE_RATE"])
        return exp_gain, stone_gain

    @staticmethod
    def add_item_to_bag(p: Player, name: str, cat: str, num: int, desc: str = ""):
        for it in p.bag:
            if it.name == name and it.category == cat:
                it.num += num
                return
        p.bag.append(BagItem(name=name, category=cat, num=num, desc=desc))

    @staticmethod
    def get_bag_item_count(p: Player, name: str) -> int:
        cnt = 0
        for it in p.bag:
            if it.name == name:
                cnt += it.num
        return cnt

    @staticmethod
    def consume_bag_item(p: Player, name: str, need_num: int) -> bool:
        remain = need_num
        new_bag = []
        for it in p.bag:
            if remain > 0 and it.name == name:
                if it.num > remain:
                    it.num -= remain
                    remain = 0
                    new_bag.append(it)
                else:
                    remain -= it.num
            else:
                new_bag.append(it)
        p.bag = new_bag
        return remain <= 0

    @staticmethod
    def trigger_random_city_event(p: Player) -> str:
        evt = random.choice(GAME_CONFIG["CITY_EVENT"])
        eff = evt["effect"]
        msg = f"\n【城镇事件】{evt['title']}：{evt['desc']}"
        if "arm_add_max" in eff:
            pass
        if "stone_low" in eff:
            p.stone_low += eff["stone_low"]
        if "stone_high" in eff:
            p.stone_high += eff["stone_high"]
        if "exp" in eff:
            p.exp += eff["exp"]
        if "arm_loss_rate" in eff:
            loss = int(p.army_count * eff["arm_loss_rate"])
            p.army_count = max(0, p.army_count - loss)
            msg += f"\n损失军队 {loss} 人"
        return msg

# ====================== 游戏逻辑类 ======================
class GameLogic:
    @staticmethod
    def cultivate_normal(p: Player) -> Tuple[bool, str]:
        cfg = GAME_CONFIG["CULTIVATE_CFG"]
        cost_zy = cfg["normal_zy_cost"]
        if p.zy < cost_zy:
            return False, f"真元不足！需要{cost_zy}点真元，请服用丹药恢复真元"
        p.zy -= cost_zy
        gain = cfg["normal_exp_gain"]
        p.exp += gain
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"普通闭关完成！消耗真元{cost_zy}，修为+{gain}"

    @staticmethod
    def cultivate_deep(p: Player) -> Tuple[bool, str]:
        cfg = GAME_CONFIG["CULTIVATE_CFG"]
        cost_high = cfg["deep_stone_high_cost"]
        if p.stone_high < cost_high:
            return False, f"上品灵石不足，深度闭关需要上品灵石×{cost_high}"
        p.stone_high -= cost_high
        gain = cfg["deep_exp_gain"]
        p.exp += gain
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"深度闭关完成！消耗上品灵石{cost_high}，修为+{gain}"

    @staticmethod
    def save_player(p: Player, save_path: str = "save.json") -> bool:
        try:
            data = dataclasses.asdict(p)
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"存档异常:{e}")
            return False

    @staticmethod
    def load_player(save_path: str = "save.json") -> Tuple[bool, Optional[Player]]:
        if not os.path.exists(save_path):
            return False, None
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                d = json.load(f)
            p = Player(**d)
            return True, p
        except Exception as e:
            print(f"读档异常:{e}")
            return False, None

    @staticmethod
    def refresh_buff_status(p: Player):
        new_buff = []
        for b in p.buffs:
            if b.duration > 0:
                b.duration -= 1
            if b.duration != 0:
                new_buff.append(b)
        p.buffs = new_buff

        new_debuff = []
        for db in p.debuffs:
            if db.duration > 0:
                db.duration -= 1
            if db.duration != 0:
                new_debuff.append(db)
        p.debuffs = new_debuff
        p.total_power = GameUtil.calc_total_power(p)

    @staticmethod
    def use_pill_item(p: Player, bag_index: int) -> Tuple[bool, str]:
        if not (0 <= bag_index < len(p.bag)):
            return False, "背包下标错误"
        item = p.bag[bag_index]
        if item.category != "丹药":
            return False, "该物品不是丹药"

        name = item.name
        if name == "淬体丹":
            p.physique += 30
            p.max_hp += 120
            msg = f"服用淬体丹，体魄+30，气血上限+120"
        elif name == "聚气丹":
            p.exp += 3200
            msg = f"服用聚气丹，修为+3200"
        elif name == "固元丹":
            p.hp = p.max_hp
            p.zy = p.max_zy
            msg = f"服用固元丹，气血真元完全回满"
        elif name == "破境丹":
            buf = BuffDebuff(name="破境丹药效", desc="突破成功率+20%", type="buff", duration=15,
                             params={"break_add_rate": 0.20})
            p.buffs.append(buf)
            msg = "服用破境丹，获得【破境丹药效】buff，突破成功率提升"
        elif name == "洗髓丹":
            p.physique += 60
            p.crit_rate += 0.04
            msg = "服用洗髓丹，体魄+60，暴击率提升！"
        elif name == "速元丹":
            p.zy = p.max_zy
            p.matk += 40
            msg = "服用速元丹，真元回满，法攻+40"
        else:
            return False, f"丹药[{name}]未实现效果"

        item.num -= 1
        if item.num <= 0:
            p.bag.pop(bag_index)
        p.total_power = GameUtil.calc_total_power(p)
        return True, msg

    @staticmethod
    def military_research(p: Player, blueprint_name: str) -> Tuple[bool, str]:
        cost_stone_high = 20 * p.territory_lv
        if p.stone_high < cost_stone_high:
            return False, f"上品灵石不足，需要{cost_stone_high}"
        p.stone_high -= cost_stone_high

        if blueprint_name == "灵能步枪蓝图":
            new_eq = EquipItem(
                name="灵能步枪", rank="宝器", slot="军工军械",
                atk_bonus=220, def_bonus=40,
                special={"arm_damage_bonus": 0.25}
            )
            p.equip_slot["军工军械"] = new_eq
            return True, "研发成功，获得【宝器】灵能步枪，装备到军工军械槽！"
        elif blueprint_name == "军阵罗盘蓝图":
            p.army_arrays.append({"name": "万灵基础军阵", "power_bonus": 0.30, "active": False})
            return True, "研发成功，获得军阵：万灵基础军阵，可进行布阵激活"
        else:
            return False, f"不存在该蓝图：{blueprint_name}"

    @staticmethod
    def unlock_array(p: Player, array_lib_idx: int) -> Tuple[bool, str]:
        lib = GAME_CONFIG["ARRAY_LIB"]
        if not (0 <= array_lib_idx < len(lib)):
            return False, "军阵编号错误"
        arr_info = lib[array_lib_idx]
        if p.stone_high < arr_info["cost_high"]:
            return False, f"上品灵石不足，需要{arr_info['cost_high']}"
        p.stone_high -= arr_info["cost_high"]
        for exist in p.army_arrays:
            if exist["name"] == arr_info["aname"]:
                return False, "已经拥有该军阵"
        p.army_arrays.append({"name": arr_info["aname"], "power_bonus": arr_info["pow_bonus"], "active": False})
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"解锁军阵【{arr_info['aname']}】！战力加成{arr_info['pow_bonus']*100}%"

    @staticmethod
    def activate_army_array(p: Player, array_idx: int) -> Tuple[bool, str]:
        if not (0 <= array_idx < len(p.army_arrays)):
            return False, "军阵编号不存在"
        arr = p.army_arrays[array_idx]
        if arr["active"]:
            return False, "该军阵已经处于激活状态"
        arr["active"] = True
        buf = BuffDebuff(
            name=arr["name"],
            desc=f"军阵加成，战力+{arr['power_bonus'] * 100:.0f}%",
            type="buff",
            duration=0,
            params={"power_mult": 1.0 + arr["power_bonus"]}
        )
        p.buffs.append(buf)
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"成功激活军阵【{arr['name']}】，全局战力获得加成！"

    @staticmethod
    def sacrifice_nation_luck(p: Player) -> Tuple[bool, str]:
        cost = 8000
        if p.stone_low < cost:
            return False, f"下品灵石不足，需要{cost}"
        p.stone_low -= cost
        add_luck = random.randint(30, 120)
        p.nation_luck += add_luck
        return True, f"祭祀完成！国运值 +{add_luck}，当前国运{p.nation_luck}"

    @staticmethod
    def sect_mission(p: Player) -> Tuple[bool, str, int]:
        gain_exp = random.randint(800, 3000)
        stone_gain = random.randint(100, 600)
        p.exp += gain_exp
        p.stone_low += stone_gain
        roll = random.random()
        if roll < 0.08 and p.sect_pos_idx < len(GAME_CONFIG["SECT_POS"]) - 1:
            p.sect_pos_idx += 1
            return True, f"宗门任务完成！修为+{gain_exp},灵石+{stone_gain}，职位晋升！", gain_exp
        return True, f"宗门任务完成！修为+{gain_exp},下品灵石+{stone_gain}", gain_exp

    @staticmethod
    def turn_battle(p: Player, enemy_name: str, enemy_power: float, enemy_hp: int) -> Tuple[bool, int, List[str]]:
        drop_list = []
        e_hp = enemy_hp
        my_hp = p.hp
        debuff_mod = GameUtil.get_debuff_mod(p)

        while e_hp > 0 and my_hp > 0:
            dmg_base = (p.patk + p.matk) * debuff_mod
            crit_flag = random.random() <= p.crit_rate
            final_dmg = dmg_base
            if crit_flag:
                final_dmg *= p.crit_mult
            if random.random() <= p.break_def:
                final_dmg *= 1.35
            e_hp -= final_dmg
            if e_hp <= 0:
                break

            e_dmg = enemy_power * 0.04
            reduce = p.tough_dmg_reduce
            real_e_dmg = e_dmg * (1 - reduce)
            if random.random() <= p.dodge_rate:
                real_e_dmg = 0
            my_hp -= real_e_dmg

        win = e_hp <= 0
        if win and enemy_name not in p.enemy_book:
            p.enemy_book.append(enemy_name)
        if win:
            lib = None
            for e in GAME_CONFIG["ENEMY_LIB"]:
                if e["ename"] == enemy_name:
                    lib = e
                    break
            if lib:
                for d in lib["drop"]:
                    if random.random() < 0.75:
                        drop_list.append(d)
        return win, int(my_hp), drop_list

    @staticmethod
    def realm_break(p: Player) -> Tuple[bool, str]:
        cfg = GAME_CONFIG["REALM_LIST"]
        if p.realm_idx >= len(cfg) - 1:
            return False, "已是最高境界"
        next_cfg = cfg[p.realm_idx + 1]
        add_rate = 0.0
        for b in p.buffs:
            if "break_add_rate" in b.params:
                add_rate += b.params["break_add_rate"]
        need_exp = int(next_cfg["exp_need"] * (1.0 - add_rate))
        if p.exp < need_exp:
            return False, f"修为不足，需要{need_exp}(基础{next_cfg['exp_need']})"
        p.exp -= need_exp
        p.realm_idx += 1
        p.max_hp += next_cfg["hp_add"]
        p.hp = p.max_hp
        p.max_zy += next_cfg["zy_add"]
        p.zy = p.max_zy
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"突破成功！晋升【{next_cfg['name']}】"

    @staticmethod
    def equip_item(p: Player, bag_idx: int) -> Tuple[bool, str]:
        if not (0 <= bag_idx < len(p.bag)):
            return False, "背包序号错误"
        it = p.bag[bag_idx]
        if it.category != "装备":
            return False, "该物品不是装备"
        eq = EquipItem(name=it.name, rank=it.desc, slot=it.category, atk_bonus=100, def_bonus=30)
        old = p.equip_slot.get(eq.slot, None)
        p.equip_slot[eq.slot] = eq
        it.num -= 1
        if it.num <= 0:
            p.bag.pop(bag_idx)
        if old is not None:
            GameUtil.add_item_to_bag(p, old.name, "装备", 1, old.rank)
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"穿戴【{eq.name}】完成！旧装备放回背包"

    @staticmethod
    def un_equip(p: Player, slot_key: str) -> Tuple[bool, str]:
        if slot_key not in p.equip_slot or p.equip_slot[slot_key] is None:
            return False, "该槽位没有装备"
        eq = p.equip_slot[slot_key]
        GameUtil.add_item_to_bag(p, eq.name, "装备", 1, eq.rank)
        p.equip_slot[slot_key] = None
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"卸下【{eq.name}】放回背包"

    @staticmethod
    def shop_buy(p: Player, goods_idx: int) -> Tuple[bool, str]:
        goods_list = GAME_CONFIG["SHOP_GOODS"]
        if not (0 <= goods_idx < len(goods_list)):
            return False, "商品编号错误"
        g = goods_list[goods_idx]
        cl, ch = g["cost_low"], g["cost_high"]
        if p.stone_low < cl or p.stone_high < ch:
            return False, f"灵石不足！需要下品{cl} 上品{ch}"
        p.stone_low -= cl
        p.stone_high -= ch
        GameUtil.add_item_to_bag(p, g["g_name"], g["g_cat"], g["g_num"])
        return True, f"购买成功：{g['g_name']}"

    @staticmethod
    def death_penalty(p: Player) -> int:
        lose_exp = int(p.exp * 0.15)
        p.exp -= lose_exp
        if p.exp < 0:
            p.exp = 0
        p.hp = int(p.max_hp * 0.25)
        p.debuffs.append(BuffDebuff(name="重伤", desc="全属性下降15%", type="debuff", duration=8, params={"all_down": 0.15}))
        p.total_power = GameUtil.calc_total_power(p)
        return lose_exp

    @staticmethod
    def territory_upgrade(p: Player) -> Tuple[bool, str]:
        cfg_list = GAME_CONFIG["TERRITORY_CFG"]
        next_lv = p.territory_lv + 1
        if next_lv > len(cfg_list):
            return False, "领土已经满级"
        cfg = cfg_list[next_lv - 1]
        if p.stone_low < cfg["cost_low"] or p.stone_high < cfg["cost_high"]:
            return False, f"资源不足！需要下品{cfg['cost_low']}，上品{cfg['cost_high']}"
        p.stone_low -= cfg["cost_low"]
        p.stone_high -= cfg["cost_high"]
        p.territory_lv = next_lv
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"领土升级成功！现在为【{cfg['name']}】，军队上限:{cfg['arm_max']}"

    @staticmethod
    def conscript_army(p: Player, add_num: int) -> Tuple[bool, str]:
        arm_max = GameUtil.get_arm_max(p)
        if p.army_count >= arm_max:
            return False, f"军队已达上限{arm_max}，请升级领土"
        real_add = min(add_num, arm_max - p.army_count)
        cost = real_add * 12
        if p.stone_low < cost:
            return False, f"灵石不足，征兵{real_add}人需要下品{cost}"
        p.stone_low -= cost
        p.army_count += real_add
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"征兵完成！新增{real_add}名士兵，当前总军队{p.army_count}/{arm_max}"

    @staticmethod
    def do_forge(p: Player, recipe_idx: int) -> Tuple[bool, str]:
        rec = GAME_CONFIG["FORGE_RECIPE"][recipe_idx]
        for mat_name, need_cnt in rec["need"].items():
            if GameUtil.get_bag_item_count(p, mat_name) < need_cnt:
                return False, f"材料不足：{mat_name}，需要{need_cnt}"
        for mat_name, need_cnt in rec["need"].items():
            GameUtil.consume_bag_item(p, mat_name, need_cnt)
        eq = EquipItem(name=rec["r_name"], rank="宝器", slot=rec["slot"], atk_bonus=rec["atk"], def_bonus=rec["def"])
        p.equip_slot[rec["slot"]] = eq
        p.total_power = GameUtil.calc_total_power(p)
        return True, f"锻造成功！产出【{rec['r_name']}】自动装备"

    @staticmethod
    def do_alchemy(p: Player, recipe_idx: int) -> Tuple[bool, str]:
        rec = GAME_CONFIG["ALCHEMY_RECIPE"][recipe_idx]
        for mat_name, need_cnt in rec["need"].items():
            if GameUtil.get_bag_item_count(p, mat_name) < need_cnt:
                return False, f"材料不足：{mat_name}，需要{need_cnt}"
        for mat_name, need_cnt in rec["need"].items():
            GameUtil.consume_bag_item(p, mat_name, need_cnt)
        GameUtil.add_item_to_bag(p, rec["p_name"], "丹药", 1)
        return True, f"炼丹成功！产出【{rec['p_name']}】存入背包"

# ====================== UI 面板 ======================
class GamePanel:
    @staticmethod
    def panel_status(p: Player):
        print("\n" + "=" * 65)
        print(f"【个人状态】境界:{GameUtil.get_realm_name(p)}｜战力:{p.total_power}")
        print(f"修为:{p.exp}｜气血:{p.hp}/{p.max_hp}｜真元:{p.zy}/{p.max_zy}")
        print(f"体魄:{p.physique}｜物攻:{p.patk}｜法攻:{p.matk}")
        print(f"下品灵石:{p.stone_low}｜上品灵石:{p.stone_high}")
        print(f"buff:{len(p.buffs)}  debuff:{len(p.debuffs)} 妖兽图鉴:{len(p.enemy_book)}/{len(GAME_CONFIG['ENEMY_LIB'])}")
        print("-" * 30 + "【辅助国运】" + "-" * 30)
        print(f"领土:{GameUtil.get_territory_name(p)}｜军队:{p.army_count}/{GameUtil.get_arm_max(p)}｜国运:{p.nation_luck}")
        print(f"宗门职位:{GAME_CONFIG['SECT_POS'][p.sect_pos_idx]}")
        print("=" * 65)

    @staticmethod
    def panel_bag(p: Player):
        print("\n=====背包=====")
        if len(p.bag) == 0:
            print("背包空空如也")
            return
        for idx, it in enumerate(p.bag):
            print(f"[{idx+1}] {it.name} ×{it.num} 【{it.category}】 {it.desc}")

    @staticmethod
    def panel_nation(p: Player):
        print("\n=====【辅助】国运军工面板=====")
        print(f"国运值:{p.nation_luck} 领土等级:{p.territory_lv}【{GameUtil.get_territory_name(p)}】")
        print(f"军队兵力：{p.army_count}/{GameUtil.get_arm_max(p)}")
        print("已解锁军阵：")
        for i, arr in enumerate(p.army_arrays):
            stat = "✅已激活" if arr["active"] else "⭕未激活"
            print(f"[{i+1}] {arr['name']} 加成{arr['power_bonus']*100:.0f}% {stat}")

    @staticmethod
    def panel_sect_court(p: Player):
        print("\n=====【辅助】宗门大殿=====")
        print(f"当前职位：{GAME_CONFIG['SECT_POS'][p.sect_pos_idx]}")

    @staticmethod
    def panel_battle_log(win: bool, remain_hp: int, drops: List[str]):
        if win:
            print("🎉战斗胜利！")
            print(f"剩余气血:{remain_hp}")
            if len(drops) > 0:
                print("战利品：", "、".join(drops))
            else:
                print("本次无掉落")
        else:
            print("💀战斗失败，身受重伤！")

    @staticmethod
    def panel_enemy_book(p: Player):
        print("\n=====妖兽图鉴=====")
        total = len(GAME_CONFIG["ENEMY_LIB"])
        unlock = len(p.enemy_book)
        print(f"已解锁 {unlock}/{total}")
        for lib_item in GAME_CONFIG["ENEMY_LIB"]:
            mark = "✅" if lib_item["ename"] in p.enemy_book else "🔒"
            print(f"{mark} {lib_item['ename']}")

    @staticmethod
    def panel_shop():
        print("\n=====修仙商行=====")
        goods = GAME_CONFIG["SHOP_GOODS"]
        for idx, g in enumerate(goods):
            print(f"[{idx+1}] {g['g_name']}｜下品:{g['cost_low']} 上品:{g['cost_high']}")

    @staticmethod
    def panel_equip_slot(p: Player):
        print("\n=====已穿戴装备槽=====")
        for k, v in p.equip_slot.items():
            name = v.name if v else "空"
            print(f"[{k}] : {name}")

    @staticmethod
    def panel_forge_recipe():
        print("\n=====锻造配方=====")
        for i, r in enumerate(GAME_CONFIG["FORGE_RECIPE"]):
            mat_text = ",".join([f"{k}×{v}" for k, v in r["need"].items()])
            print(f"[{i+1}] {r['r_name']}｜材料:{mat_text}")

    @staticmethod
    def panel_alchemy_recipe():
        print("\n=====炼丹配方=====")
        for i, r in enumerate(GAME_CONFIG["ALCHEMY_RECIPE"]):
            mat_text = ",".join([f"{k}×{v}" for k, v in r["need"].items()])
            print(f"[{i+1}] {r['p_name']}｜材料:{mat_text}")

    @staticmethod
    def panel_array_lib():
        print("\n=====军阵库(解锁新军阵)=====")
        for i, a in enumerate(GAME_CONFIG["ARRAY_LIB"]):
            print(f"[{i+1}] {a['aname']}｜加成{a['pow_bonus']*100}%｜消耗上品{a['cost_high']}")

# ====================== 菜单系统 ======================
class GameMenu:
    @staticmethod
    def main_menu(p: Player):
        while True:
            GameLogic.refresh_buff_status(p)
            GamePanel.panel_status(p)
            print("""
==========【个人修仙｜主线】==========
1 闭关修炼（打坐获取修为）
2 外出狩猎战斗
3 尝试境界突破
4 查看背包｜使用丹药
5 装备管理
6 妖兽图鉴
7 修仙商行

==========【辅助玩法｜非必需】==========
8 工坊｜锻造&炼丹
9 国运军工(领土/征兵/军阵)
10 宗门大殿
11 城镇随机事件

==========【系统】==========
12 存档 / 读档
0 退出游戏
""")
            op = input("请输入选项：").strip()
            if op == "0":
                print("游戏退出，记得存档！")
                break
            elif op == "1":
                GameMenu.sub_cultivate(p)
            elif op == "2":
                GameMenu.sub_battle(p)
            elif op == "3":
                ok, msg = GameLogic.realm_break(p)
                print(msg)
                input("回车继续...")
            elif op == "4":
                GameMenu.sub_bag(p)
            elif op == "5":
                GameMenu.sub_equip(p)
            elif op == "6":
                GamePanel.panel_enemy_book(p)
                input("回车...")
            elif op == "7":
                GameMenu.sub_shop(p)
            elif op == "8":
                GameMenu.sub_workshop(p)
            elif op == "9":
                GameMenu.sub_nation(p)
            elif op == "10":
                GameMenu.sub_sect(p)
            elif op == "11":
                evt_msg = GameUtil.trigger_random_city_event(p)
                print(evt_msg)
                input("回车...")
            elif op == "12":
                print("\n1保存游戏  2读取存档")
                subop = input("请选择：").strip()
                if subop == "1":
                    succ = GameLogic.save_player(p)
                    print("✅存档成功" if succ else "❌存档失败")
                elif subop == "2":
                    ok, new_p = GameLogic.load_player()
                    if ok:
                        p = new_p
                        print("✅读档成功")
                    else:
                        print("❌读档失败，无存档文件")
                input("回车继续...")
            GameLogic.refresh_buff_status(p)

    @staticmethod
    def sub_cultivate(p: Player):
        while True:
            print("\n=====闭关修炼室=====")
            print(f"当前真元 {p.zy}/{p.max_zy}")
            print("1普通闭关（消耗真元获取修为）")
            print("2深度闭关（消耗上品灵石，高额修为）")
            print("0 返回主菜单")
            sel = input("选择：").strip()
            if sel == "0":
                break
            elif sel == "1":
                ok, msg = GameLogic.cultivate_normal(p)
                print(msg)
            elif sel == "2":
                ok, msg = GameLogic.cultivate_deep(p)
                print(msg)
            input("回车继续...")

    @staticmethod
    def sub_bag(p: Player):
        while True:
            GamePanel.panel_bag(p)
            print("\n1 使用丹药 | 0 返回")
            sel = input("选择：").strip()
            if sel == "0":
                break
            elif sel == "1":
                idx_str = input("输入要使用物品序号：").strip()
                if idx_str.isdigit():
                    idx = int(idx_str) - 1
                    ok, msg = GameLogic.use_pill_item(p, idx)
                    print(f">> {msg}")
            input("回车...")

    @staticmethod
    def sub_nation(p: Player):
        while True:
            GamePanel.panel_nation(p)
            print("""
1 研发军工(灵能步枪/军阵罗盘)
2 执行国运祭祀
3 激活已有军阵
4 解锁新军阵
5 领土升级
6 征兵扩军
0 返回
""")
            opt = input("选择：").strip()
            if opt == "0":
                break
            elif opt == "1":
                print("1研发灵能步枪蓝图｜2研发军阵罗盘蓝图")
                ch = input("选择：").strip()
                if ch == "1":
                    ok, msg = GameLogic.military_research(p, "灵能步枪蓝图")
                elif ch == "2":
                    ok, msg = GameLogic.military_research(p, "军阵罗盘蓝图")
                else:
                    ok, msg = False, "无效选择"
                print(msg)
            elif opt == "2":
                ok, msg = GameLogic.sacrifice_nation_luck(p)
                print(msg)
            elif opt == "3":
                s = input("输入军阵编号：").strip()
                if s.isdigit():
                    aidx = int(s) - 1
                    ok, msg = GameLogic.activate_army_array(p, aidx)
                    print(msg)
            elif opt == "4":
                GamePanel.panel_array_lib()
                sid = input("输入解锁军阵编号：").strip()
                if sid.isdigit():
                    sidx = int(sid) - 1
                    ok, msg = GameLogic.unlock_array(p, sidx)
                    print(msg)
            elif opt == "5":
                ok, msg = GameLogic.territory_upgrade(p)
                print(msg)
            elif opt == "6":
                num_s = input("输入征兵人数：").strip()
                if num_s.isdigit():
                    num = int(num_s)
                    ok, msg = GameLogic.conscript_army(p, num)
                    print(msg)
            input("回车继续...")

    @staticmethod
    def sub_sect(p: Player):
        while True:
            GamePanel.panel_sect_court(p)
            print("1接取宗门任务｜0返回")
            opt = input("选择：").strip()
            if opt == "0":
                break
            if opt == "1":
                ok, msg, _ = GameLogic.sect_mission(p)
                print(msg)
            input("回车继续...")

    @staticmethod
    def sub_battle(p: Player):
        print("\n---外出狩猎妖兽---")
        enemy_info = random.choice(GAME_CONFIG["ENEMY_LIB"])
        ename = enemy_info["ename"]
        enemy_pow = p.total_power * enemy_info["pow_rate"]
        enemy_hp = int(enemy_pow * enemy_info["hp_rate"])
        print(f"遭遇【{ename}】！战力:{enemy_pow:.1f} 血量:{enemy_hp}")
        input("按回车开战！")
        win, remain_hp, drops = GameLogic.turn_battle(p, ename, enemy_pow, enemy_hp)
        GamePanel.panel_battle_log(win, remain_hp, drops)
        if not win:
            lose_exp = GameLogic.death_penalty(p)
            print(f"死亡惩罚：损失修为 {lose_exp}，陷入重伤debuff(全属性‑15%)")
        else:
            for d in drops:
                if "×" in d:
                    name, numstr = d.split("×")
                    num = int(numstr)
                    GameUtil.add_item_to_bag(p, name.strip(), "战利品", num)
                else:
                    GameUtil.add_item_to_bag(p, d, "战利品", 1)
            print("战利品已存入背包！")
        p.hp = remain_hp
        input("回车返回...")

    @staticmethod
    def sub_shop(p: Player):
        while True:
            GamePanel.panel_shop()
            print("\n输入商品编号购买，0返回")
            s = input("选择：").strip()
            if s == "0":
                break
            if s.isdigit():
                gid = int(s) - 1
                ok, msg = GameLogic.shop_buy(p, gid)
                print(msg)
            input("回车...")

    @staticmethod
    def sub_equip(p: Player):
        while True:
            GamePanel.panel_equip_slot(p)
            print("\n1穿戴背包装备｜2拆卸槽位装备｜0返回")
            sel = input("选择：").strip()
            if sel == "0":
                break
            elif sel == "1":
                GamePanel.panel_bag(p)
                idx_s = input("输入背包装备序号：").strip()
                if idx_s.isdigit():
                    i = int(idx_s) - 1
                    ok, msg = GameLogic.equip_item(p, i)
                    print(msg)
            elif sel == "2":
                slot = input("输入槽位名称(军工军械/武器/防具)：").strip()
                ok, msg = GameLogic.un_equip(p, slot)
                print(msg)
            input("回车...")

    @staticmethod
    def sub_workshop(p: Player):
        while True:
            print("\n=====工坊=====")
            print("1锻造｜2炼丹｜0返回")
            ch = input("选择：").strip()
            if ch == "0":
                break
            elif ch == "1":
                GamePanel.panel_forge_recipe()
                ri = input("输入锻造配方编号：").strip()
                if ri.isdigit():
                    ridx = int(ri) - 1
                    ok, msg = GameLogic.do_forge(p, ridx)
                    print(msg)
            elif ch == "2":
                GamePanel.panel_alchemy_recipe()
                ri = input("输入炼丹配方编号：").strip()
                if ri.isdigit():
                    ridx = int(ri) - 1
                    ok, msg = GameLogic.do_alchemy(p, ridx)
                    print(msg)
            input("回车...")

# ====================== 主函数 ======================
def main():
    print("======【个人修仙为主｜辅助国运为辅】======")
    player = Player()
    player.bag.append(BagItem(name="淬体丹", category="丹药", num=3, desc="提升体魄气血"))
    player.bag.append(BagItem(name="聚气丹", category="丹药", num=2, desc="增加修为"))
    player.bag.append(BagItem(name="固元丹", category="丹药", num=1, desc="回满气血真元"))
    player.bag.append(BagItem(name="破境丹", category="丹药", num=1, desc="突破buff"))
    player.bag.append(BagItem(name="洗髓丹", category="丹药", num=1, desc="体魄暴击"))
    player.bag.append(BagItem(name="速元丹", category="丹药", num=1, desc="真元法攻"))
    player.bag.append(BagItem(name="灵草", category="材料", num=40, desc="炼丹材料"))
    player.bag.append(BagItem(name="妖兽兽核", category="材料", num=25, desc="锻造炼丹材料"))
    player.bag.append(BagItem(name="宝器碎片", category="材料", num=8, desc="锻造高级装备"))

    exp_off, stone_off = GameUtil.calc_offline_gain(player)
    if exp_off > 0 or stone_off > 0:
        print(f"\n📜离线收益：修为+{exp_off}，下品灵石+{stone_off}")
        player.exp += exp_off
        player.stone_low += stone_off

    while True:
        GameLogic.refresh_buff_status(player)
        GameMenu.main_menu(player)
        break

# ====================== Kivy 终端模拟器 ======================
import threading
import queue
import builtins
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

class Terminal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=2, padding=4)
        Window.clearcolor = (0, 0, 0, 1)

        self.scroll = ScrollView(size_hint=(1, 0.9))
        self.output_label = Label(
            text='',
            font_name='DroidSansFallback',
            font_size=14,
            color=(1, 1, 1, 1),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        self.output_label.bind(width=lambda *x: setattr(self.output_label, 'text_size', (self.output_label.width, None)))
        self.output_label.bind(texture_size=lambda *x: setattr(self.output_label, 'height', self.output_label.texture_size[1]))
        self.scroll.add_widget(self.output_label)
        self.add_widget(self.scroll)

        self.input_line = TextInput(
            hint_text='> ',
            multiline=False,
            font_name='DroidSansFallback',
            font_size=16,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            size_hint=(1, 0.1)
        )
        self.input_line.bind(on_text_validate=self.on_input)
        self.add_widget(self.input_line)

        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()

        builtins.input = self.custom_input
        builtins.print = self.custom_print

        self.game_thread = threading.Thread(target=main, daemon=True)
        self.game_thread.start()

        Clock.schedule_interval(self.update_output, 0.1)

    def custom_print(self, *args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        text = sep.join(str(a) for a in args) + end
        self.output_queue.put(text)

    def custom_input(self, prompt=''):
        if prompt:
            self.output_queue.put(prompt)
        return self.input_queue.get()

    def on_input(self, instance):
        text = instance.text.strip()
        instance.text = ''
        self.input_queue.put(text)

    def update_output(self, dt):
        try:
            while True:
                text = self.output_queue.get_nowait()
                self.output_label.text += text
                self.scroll.scroll_y = 0
        except queue.Empty:
            pass

class TerminalApp(App):
    def build(self):
        return Terminal()

if __name__ == '__main__':
    TerminalApp().run()