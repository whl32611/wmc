import json
from pathlib import Path

from dreamforge import DreamForge, Idea, serialize_idea, save_idea


def test_seeded_generation_is_deterministic() -> None:
    assert DreamForge(seed=7).generate() == DreamForge(seed=7).generate()


def test_pitch_contains_strategy_fields() -> None:
    idea = Idea(
        name="赛博画布",
        domain="创作",
        problem="创意记录分散且难回顾",
        target_user="内容创作者",
        premise="通过故事化叙事引导用户坚持",
        twist="所有操作都可以离线完成",
        tech_stack=["React", "Node.js", "Supabase", "FFmpeg"],
        business_model="模板市场抽佣 + Pro 订阅",
        mvp_roadmap=["第 1 周", "第 2 周", "第 3 周", "第 4 周"],
    )
    pitch = idea.pitch()
    assert "技术栈推荐" in pitch
    assert "商业模式建议" in pitch
    assert "MVP 路线图" in pitch


def test_save_and_serialize_include_enhanced_fields(tmp_path: Path) -> None:
    idea = DreamForge(seed=3).generate()
    payload = serialize_idea(idea)
    assert isinstance(payload["tech_stack"], list)
    assert payload["business_model"]
    assert len(payload["mvp_roadmap"]) == 4

    target = tmp_path / "idea.json"
    save_idea(idea, target)
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["name"] == payload["name"]
