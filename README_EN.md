<p align="center"><strong>Independent student project by a BUPT AI student</strong> · Follow for updates and collaboration</p>
<p align="center"><a href="README.md">简体中文</a> · <a href="README_EN.md">English</a></p>

<h1 align="center">Hold My Wallet · 先别付钱</h1>

<p align="center"><strong>Make the known costs clear, surface what is still unknown, and then decide.</strong></p>
<p align="center">An AI assistant skill for shopping promotions, subscriptions, installment plans, rental agreements, and service contracts. Use it with any assistant that supports Agent Skills, or provide the files as ordinary context.</p>
<p align="center"><img alt="Validate Skill: passing" src="https://img.shields.io/badge/Validate%20Skill-passing-brightgreen"> <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow"></p>

If it helps you avoid an impulse purchase or catch an important unknown before paying, consider giving the project a ⭐ Star or following for updates. No star count is displayed here.

## What it helps with

| Situation | How Hold My Wallet helps |
| --- | --- |
| A “limited-time” discount is pressuring you | Separates the displayed price, promotion terms, checkout total, and missing evidence. |
| A free trial may renew | Lists the renewal date, price, cancellation route, and what still needs confirmation. |
| An installment looks cheap per month | Calculates the total from the numbers you provide and calls out fees that are not stated. |
| You are reviewing a lease or service contract | Extracts obligations, fees, deadlines, renewal, termination, and penalty clauses without declaring them legally valid or invalid. |

## Install

Give this instruction to your AI assistant:

```text
Install the public repository https://github.com/yifanchen12/hold-my-wallet as an Agent Skill. Keep its SKILL.md and references together.
```

If your assistant does not support skill installation, download the repository and provide `SKILL.md` plus the relevant reference page as context.

Try:

```text
Use Hold My Wallet to compare this subscription offer. Separate the quoted terms, my assumptions, your inferences, and the unknowns. Do not guess missing fees.
```

## A typical answer

1. **Evidence** — short quotes from the page or contract, with their location.
2. **User-provided details** — facts you supplied, labeled as not independently verified.
3. **Inference** — arithmetic or comparisons grounded in the material.
4. **Unknowns** — missing conditions that could change the decision.
5. **Next step** — a low-pressure verification or comparison; you make the purchase decision.

### Example

Input: “The plan is ¥39 per month for 12 months, with a ¥20 setup fee. Is that really ¥39?”

Output: “**Known from your description:** 12 monthly payments of ¥39 and a ¥20 setup fee. **Calculated total:** ¥39 × 12 + ¥20 = **¥488**. **Unknown:** tax, cancellation charges, payment fees, and whether the setup fee is already included. This calculation is not a quote from the seller.”

For money calculations, the included Python script uses explicit inputs and decimal arithmetic; it preserves supplied precision instead of silently rounding to two decimal places. It does not look up prices or invent missing charges.

## Reference library

The knowledge base contains **100 references** across consumer rules, promotion evidence, subscriptions, installment costs, contract reading, and behavioral research. Each entry carries a source and scope note. Load only the relevant page and verify the current original source.

- [Knowledge base guide](references/knowledge/README.md)
- [Core 100-item source index](references/knowledge/来源索引.md)
- [Promotion evidence](references/knowledge/价格宣传与促销证据.md)
- [Subscriptions and installment plans](references/knowledge/订阅与分期付款核对.md)
- [Contract clauses and consumer rights](references/knowledge/合同文字与消费者权益.md)

## Limits and privacy

- It does not verify historical prices, inventory, merchant intent, or hidden checkout conditions.
- It does not determine that a merchant committed fraud or provide case-specific legal, tax, or financial advice.
- It cannot guarantee a refund, cancellation, or complaint outcome.
- Share only the excerpt needed. Remove names, addresses, account identifiers, payment details, and other sensitive information first.
- Calculations are only as complete as the values and fee terms you provide.

## Development and license

Run the validator and calculator tests with Python 3:

```bash
python tests/validate_skill.py
python -m unittest discover -s tests -p "test_*.py" -v
```

MIT License. See [LICENSE](LICENSE).
