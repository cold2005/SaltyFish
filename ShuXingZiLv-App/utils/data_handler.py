import json
import os
import uuid
import random
from datetime import datetime
from typing import Dict, List, Optional, Union
from PIL import Image
import io

# ==================== 路径配置（固定，后续无需修改）====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
DATA_DIR = os.path.join(BASE_DIR, "data")  # 数据根目录
USER_DATA_PATH = os.path.join(DATA_DIR, "user_data.json")  # JSON数据文件路径
RECORD_IMAGE_DIR = os.path.join(DATA_DIR, "records")  # 成长记录图片目录


# ==================== 初始化配置（首次运行自动创建目录和默认数据）====================
def init_data_env():
    """初始化数据环境：创建目录 + 生成默认JSON数据（优化日志输出）"""
    # 创建data目录和records子目录（exist_ok=True 已处理重复创建）
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECORD_IMAGE_DIR, exist_ok=True)

    # 只在文件不存在时打印日志
    if not os.path.exists(USER_DATA_PATH):
        default_data = generate_default_data()
        write_data(default_data)
        print(f"✅ 初始化数据成功：创建 {USER_DATA_PATH}")


def generate_default_data() -> Dict:
    """生成默认JSON数据（支持多级任务树，包含parent_id）"""
    # 生成默认段位规则（S/A/B/C/D/E/F）
    rank_rules = [
        {"rank": "S", "min": 90, "max": 100},
        {"rank": "A", "min": 80, "max": 89},
        {"rank": "B", "min": 70, "max": 79},
        {"rank": "C", "min": 60, "max": 69},
        {"rank": "D", "min": 50, "max": 59},
        {"rank": "E", "min": 40, "max": 49},
        {"rank": "F", "min": 0, "max": 39}
    ]

    # 默认能力项
    default_abilities = [
        {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "学习能力", "value": 60},
        {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "执行能力", "value": 55},
        {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "自律能力", "value": 50},
        {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "创新能力", "value": 70}
    ]

    return {
        "targets": [
            # 默认示例目标（新增parent_id="root"，支持多级任务树）
            {
                "id": f"target_{uuid.uuid4().hex[:8]}",
                "name": "完成Python基础学习",
                "deadline": "2025-12-31",
                "status": "未开始",
                "reward_points": 50,
                "parent_id": "root"  # 根节点标识
            }
        ],
        "rating_systems": [
            {
                "id": f"rating_{uuid.uuid4().hex[:8]}",
                "name": "综合能力",
                "abilities": default_abilities,
                "rank_rules": rank_rules
            }
        ],
        "growth_records": [],  # 初始无成长记录
        "points_account": {
            "total": 0,
            "records": []
        }
    }


# ==================== 核心工具函数（后续模块调用入口）====================
def read_data() -> Dict:
    """读取user_data.json数据，返回字典格式（兼容多级任务树）"""
    # 确保数据环境已初始化
    init_data_env()

    try:
        with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 兼容处理：补充缺失字段（含parent_id）
        data = complement_data_structure(data)
        return data
    except json.JSONDecodeError:
        print("⚠️  JSON数据格式错误，使用默认数据覆盖")
        default_data = generate_default_data()
        write_data(default_data)
        return default_data
    except Exception as e:
        print(f"❌ 读取数据失败：{str(e)}")
        return generate_default_data()


def write_data(data: Dict) -> bool:
    """将字典数据写入user_data.json，返回写入结果（成功True/失败False）"""
    try:
        with open(USER_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ 写入数据失败：{str(e)}")
        return False


def save_image(image_data: Union[bytes, io.BytesIO]) -> Optional[str]:
    """
    保存图片到data/records目录，返回图片相对路径（供JSON存储）
    :param image_data: 图片二进制数据 或 BytesIO对象
    :return: 成功返回相对路径（如"data/records/1740000000_123456.jpg"），失败返回None
    """
    try:
        # 生成文件名：时间戳_8位随机数.jpg
        timestamp = int(datetime.now().timestamp())
        random_num = random.randint(100000, 999999)
        filename = f"{timestamp}_{random_num}.jpg"
        image_abs_path = os.path.join(RECORD_IMAGE_DIR, filename)

        # 处理图片数据并保存（确保格式正确）
        with Image.open(image_data) as img:
            # 自动转换为RGB格式（处理透明图片）
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(image_abs_path, "JPEG", quality=90)

        # 返回相对路径（项目根目录为基准）
        relative_path = os.path.relpath(image_abs_path, BASE_DIR)
        return relative_path
    except Exception as e:
        print(f"❌ 保存图片失败：{str(e)}")
        return None


def complement_data_structure(data: Dict) -> Dict:
    """兼容旧数据：补充缺失的字段（重点添加parent_id支持多级任务树）"""
    # 1. 检查并补充targets字段（核心：为旧目标添加parent_id）
    if "targets" not in data:
        data["targets"] = []
    else:
        # 为所有旧目标（无parent_id）添加parent_id="root"，转为根节点
        for target in data["targets"]:
            if "parent_id" not in target:
                target["parent_id"] = "root"
            # 兼容旧字段名（如果存在旧版"reward_points"以外的字段）
            if "points" not in target and "reward_points" in target:
                target["points"] = target["reward_points"]  # 统一字段名便于后续处理

    # 2. 检查并补充rating_systems字段（保持原有逻辑）
    if "rating_systems" not in data:
        data["rating_systems"] = [generate_default_data()["rating_systems"][0]]
    else:
        for rs in data["rating_systems"]:
            if "rank_rules" not in rs:
                rs["rank_rules"] = generate_default_data()["rating_systems"][0]["rank_rules"]
            if "abilities" not in rs:
                rs["abilities"] = []

    # 3. 检查并补充growth_records字段（保持原有逻辑）
    if "growth_records" not in data:
        data["growth_records"] = []

    # 4. 检查并补充points_account字段（保持原有逻辑）
    if "points_account" not in data:
        data["points_account"] = {"total": 0, "records": []}
    else:
        if "total" not in data["points_account"]:
            data["points_account"]["total"] = 0
        if "records" not in data["points_account"]:
            data["points_account"]["records"] = []

    return data