#!/usr/bin/env python3
"""DreamForge: 创意软件点子锻造器（增强版）。"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ADJECTIVES = ["量子", "赛博", "像素", "梦境", "流光", "星尘", "荒野", "秘境"]
PRODUCTS = ["笔记", "画布", "地图", "信使", "实验室", "工作台", "图鉴", "播客"]
DOMAINS = ["学习", "健康", "创作", "游戏", "效率", "旅行", "社交", "理财"]
MECHANICS = [
    "用 AI 做每日挑战",
    "把复杂任务拆成 3 分钟微步骤",
    "通过故事化叙事引导用户坚持",
    "让朋友互相协作打卡",
    "根据情绪推荐不同模式",
    "利用语音快速记录灵感",
    "把数据转成可视化成长轨迹",
    "每周自动生成复盘报告",
]
TWISTS = [
    "它的核心界面像一款 RPG 游戏",
    "所有操作都可以离线完成",
    "每次打开都会出现一个随机创意任务",
    "用户可以交易自己的模板与工作流",
    "系统会把失败案例也当作奖励资源",
    "支持把成果一键发布到社交平台",
    "新人模式只有一个按钮，极简上手",
    "可通过番茄钟 + 音乐进入心流",
]
PROBLEMS = [
    "用户很难长期坚持好习惯",
    "信息太多导致执行瘫痪",
    "创意记录分散且难回顾",
    "团队协作缺乏轻量流程",
    "个人成长无法被量化追踪",
]
TARGET_USERS = ["学生", "独立开发者", "产品经理", "内容创作者", "远程团队", "自由职业者"]

TECH_STACKS = {
    "学习": ["Next.js", "FastAPI", "PostgreSQL", "Redis", "OpenAI API"],
    "健康": ["Flutter", "FastAPI", "TimescaleDB", "Apple HealthKit", "Grafana"],
    "创作": ["React", "Node.js", "Supabase", "Cloudflare R2", "FFmpeg"],
    "游戏": ["Unity", "C#", "Firebase", "PlayFab", "Photon"],
    "效率": ["Tauri", "Rust", "SQLite", "Actix Web", "WebSocket"],
    "旅行": ["Vue", "Go", "PostGIS", "Mapbox", "Stripe"],
    "社交": ["React Native", "NestJS", "MongoDB", "Socket.IO", "S3"],
    "理财": ["SvelteKit", "Django", "PostgreSQL", "Plaid", "Docker"],
}

BUSINESS_MODELS = {
    "学习": "Freemium + 订阅（高级题库与 AI 导师）",
    "健康": "会员订阅 + 企业健康计划 B2B",
    "创作": "模板市场抽佣 + Pro 订阅",
    "游戏": "季票制 + 装扮内购",
    "效率": "个人订阅 + 团队席位制收费",
    "旅行": "交易佣金 + 增值服务包",
    "社交": "创作者分成 + 品牌合作",
    "理财": "高级分析订阅 + 顾问服务",
}

MVP_TEMPLATES = [
    "第 1 周：完成用户访谈 10 人，验证核心痛点。",
    "第 2 周：上线可交互原型，覆盖最小主流程。",
    "第 3 周：接入关键数据追踪，观察激活与留存。",
    "第 4 周：开放 50 位种子用户，基于反馈迭代。",
]


@dataclass
class Idea:
    name: str
    domain: str
    problem: str
    target_user: str
    premise: str
    twist: str
    tech_stack: list[str]
    business_model: str
    mvp_roadmap: list[str]

    def pitch(self) -> str:
        roadmap = "\n".join(f"  - {step}" for step in self.mvp_roadmap)
        stack = " / ".join(self.tech_stack)
        return (
            f"【{self.name}】\n"
            f"领域：{self.domain}\n"
            f"目标用户：{self.target_user}\n"
            f"要解决的问题：{self.problem}\n"
            f"核心玩法：{self.premise}。\n"
            f"亮点：{self.twist}。\n"
            f"技术栈推荐：{stack}\n"
            f"商业模式建议：{self.business_model}\n"
            f"MVP 路线图：\n{roadmap}"
        )


class DreamForge:
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def generate(self) -> Idea:
        domain = self._pick(DOMAINS)
        return Idea(
            name=f"{self._pick(ADJECTIVES)}{self._pick(PRODUCTS)}",
            domain=domain,
            problem=self._pick(PROBLEMS),
            target_user=self._pick(TARGET_USERS),
            premise=self._pick(MECHANICS),
            twist=self._pick(TWISTS),
            tech_stack=self._recommend_stack(domain),
            business_model=BUSINESS_MODELS[domain],
            mvp_roadmap=self._build_mvp_roadmap(),
        )

    def _pick(self, source: Iterable[str]) -> str:
        return self._rng.choice(list(source))

    def _recommend_stack(self, domain: str) -> list[str]:
        stack = TECH_STACKS[domain][:]
        self._rng.shuffle(stack)
        return stack[:4]

    def _build_mvp_roadmap(self) -> list[str]:
        steps = MVP_TEMPLATES[:]
        self._rng.shuffle(steps)
        return steps


def serialize_idea(idea: Idea) -> dict:
    payload = asdict(idea)
    payload["pitch"] = idea.pitch()
    return payload


def save_idea(idea: Idea, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(serialize_idea(idea), ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DreamForge - 随机生成可执行的软件创意")
    parser.add_argument("--seed", type=int, default=None, help="随机种子，便于复现结果")
    parser.add_argument("--save", type=Path, default=None, help="把创意保存为 JSON 文件")
    parser.add_argument("--json", action="store_true", help="以 JSON 直接打印到终端")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    idea = DreamForge(seed=args.seed).generate()

    if args.json:
        print(json.dumps(serialize_idea(idea), ensure_ascii=False, indent=2))
    else:
        print("✨ DreamForge 创意已出炉（增强版）！\n")
        print(idea.pitch())

    if args.save:
        save_idea(idea, args.save)
        print(f"\n💾 已保存到: {args.save}")


if __name__ == "__main__":
    main()
