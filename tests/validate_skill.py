import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
assert skill.startswith("---\nname: hold-my-wallet\ndescription:")
for required in ("scripts/cost_calculator.py", "references/", "### 目前能确认", "安全与隐私"):
    assert required in skill, f"SKILL.md 缺少协议字段: {required}"
for path in ("README.md", "README_EN.md", "LICENSE", "scripts/cost_calculator.py", "tests/test_cost_calculator.py", "examples/input.json", "examples/output.json", "references/knowledge/README.md", "references/knowledge/来源索引.md"):
    assert (ROOT / path).is_file(), f"缺少文件: {path}"
refs = list((ROOT / "references").glob("*.md"))
assert len(refs) >= 3, "场景指南至少 3 份"
cases = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8"))
assert len(cases) >= 10, "测试案例至少 10 个"
assert {case["type"] for case in cases} >= {"正常", "信息不足", "边界", "安全"}
source_index = (ROOT / "references/knowledge/来源索引.md").read_text(encoding="utf-8")
source_ids = {line.split("]", 1)[0][3:] for line in source_index.splitlines() if line.startswith("| [R")}
assert len(source_ids) >= 100, f"核心资料索引不足 100 项：{len(source_ids)}"
print(f"先别付钱结构校验通过：{len(refs)} 份场景指南，{len(cases)} 个案例，{len(source_ids)} 项资料。")
