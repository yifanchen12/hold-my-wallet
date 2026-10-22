#!/usr/bin/env python3
"""Deterministic cost totals for user-provided amounts; never estimates unknown fees."""

from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation
from typing import Any


class InputError(ValueError):
    """Raised when an amount or count is missing or invalid."""


def _amount(value: Any, field: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise InputError(f"{field}: 金额必须以字符串或整数提供")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise InputError(f"{field}: 金额格式无效") from None
    if not result.is_finite() or result < 0:
        raise InputError(f"{field}: 金额必须是有限的非负数")
    return result


def _count(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise InputError(f"{field}: 期数/次数必须是正整数")
    return value


def _rows(data: Any, field: str) -> list[dict[str, Any]]:
    if data is None:
        return []
    if not isinstance(data, list):
        raise InputError(f"{field}: 必须是数组")
    if any(not isinstance(row, dict) for row in data):
        raise InputError(f"{field}: 每项必须是对象")
    return data


def calculate(data: dict[str, Any]) -> dict[str, Any]:
    """Return totals from explicit inputs; `unknown_costs` remain unpriced."""
    if not isinstance(data, dict):
        raise InputError("输入必须是 JSON 对象")

    breakdown: list[dict[str, str]] = []
    total = Decimal("0")

    for index, row in enumerate(_rows(data.get("one_time"), "one_time"), 1):
        label = str(row.get("label") or f"一次性费用 {index}")
        amount = _amount(row.get("amount"), f"one_time[{index}].amount")
        total += amount
        breakdown.append({"label": label, "kind": "一次性", "amount": f"{amount:.2f}"})

    for index, row in enumerate(_rows(data.get("recurring"), "recurring"), 1):
        label = str(row.get("label") or f"周期费用 {index}")
        amount = _amount(row.get("amount_per_period"), f"recurring[{index}].amount_per_period")
        periods = _count(row.get("periods"), f"recurring[{index}].periods")
        line_total = amount * periods
        total += line_total
        breakdown.append({"label": label, "kind": "周期费用", "amount": f"{line_total:.2f}", "periods": str(periods)})

    for index, row in enumerate(_rows(data.get("installments"), "installments"), 1):
        label = str(row.get("label") or f"分期 {index}")
        amount = _amount(row.get("amount_per_period"), f"installments[{index}].amount_per_period")
        periods = _count(row.get("periods"), f"installments[{index}].periods")
        line_total = amount * periods
        total += line_total
        breakdown.append({"label": label, "kind": "分期", "amount": f"{line_total:.2f}", "periods": str(periods)})

    for index, row in enumerate(_rows(data.get("fees"), "fees"), 1):
        label = str(row.get("label") or f"其他费用 {index}")
        amount = _amount(row.get("amount"), f"fees[{index}].amount")
        total += amount
        breakdown.append({"label": label, "kind": "其他费用", "amount": f"{amount:.2f}"})

    comparisons: list[dict[str, str]] = []
    for index, row in enumerate(_rows(data.get("offer_comparisons"), "offer_comparisons"), 1):
        original = _amount(row.get("reference_amount"), f"offer_comparisons[{index}].reference_amount")
        offer = _amount(row.get("offer_amount"), f"offer_comparisons[{index}].offer_amount")
        comparisons.append({
            "label": str(row.get("label") or f"优惠对比 {index}"),
            "reference_amount": f"{original:.2f}",
            "offer_amount": f"{offer:.2f}",
            "difference": f"{(original - offer):.2f}",
            "note": "仅按输入数字相减；参考价是否真实、是否为历史价未核实。",
        })

    unknown_costs = data.get("unknown_costs", [])
    if not isinstance(unknown_costs, list):
        raise InputError("unknown_costs: 必须是数组")

    return {
        "currency": str(data.get("currency") or "CNY"),
        "breakdown": breakdown,
        "known_total": f"{total:.2f}",
        "unknown_costs": [str(item) for item in unknown_costs],
        "total_is_complete": len(unknown_costs) == 0 and bool(breakdown),
        "offer_comparisons": comparisons,
        "basis": "只计算用户明确提供的金额与次数；未填项目不视为 0 元。",
    }


def main() -> int:
    try:
        result = calculate(json.load(sys.stdin))
    except (InputError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
