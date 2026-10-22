# 先别付钱 · Hold My Wallet

一个帮助你在下单、续费、分期或签合同前，把已知价格算清、把关键未知项找出来的 Codex Agent Skill。

它会把页面/合同原文、你提供的信息、推断和未知项分开；涉及金额时用随附 Python 脚本按明确输入计算。它不会编造历史价格、替商家定性欺诈，也不会代替法律或财务专业意见。

## 能做什么

- 对照网购促销条件，核清页面价、优惠门槛、运费与实际结算价。
- 展开免费期、续费金额、周期与下次扣款时间。
- 合并首付、分期、手续费和明确的额外费用，避免只看月供。
- 从租房或服务合同中提取押金、续期、取消、退款和违约条款原文。
- 将未提供的金额留为未知，不把它按 0 元处理。

## 安装

将整个 `hold-my-wallet` 文件夹复制到 Codex skills 目录，然后重新打开 Codex：

- Windows：`%USERPROFILE%\.codex\skills\hold-my-wallet`
- macOS / Linux：`~/.codex/skills/hold-my-wallet`

调用示例：

```text
使用 $hold-my-wallet，帮我核对这张分期页面截图：首付 200 元、每月 100 元共 10 期，手续费 30 元。把原文证据、计算和未知项分开。
```

## 示例

`examples/input.json` 是脚本输入，`examples/output.json` 是对应输出。已知金额为 1230 元，但提前结清费用未知，所以结果明确标为不完整。

本地计算：

```bash
python scripts/cost_calculator.py < examples/input.json
```

PowerShell 可用：

```powershell
Get-Content -Raw examples/input.json | python scripts/cost_calculator.py
```

只接受明确金额与次数；优惠参考价只做数字相减，不验证参考价真假。输入格式详见 `scripts/cost_calculator.py`。

## 验证

```bash
python -m unittest discover -s tests -v
python tests/validate_skill.py
```

案例清单在 `tests/cases.json`，覆盖正常、信息不足、边界和安全情形。

## 局限与隐私

- 不联网查价、不登录账户、不读取历史订单，也不验证商家库存、促销真实性或历史价格。
- 合同分析是条款提取和问题清单，不是法律意见；复杂或高风险事项应找当地专业人士核实。
- 不要粘贴密码、验证码、银行卡完整号码或身份证完整号码；先遮挡再分享。
- 计算器只在本机运行，不联网、不保存输入；对未提供的税费、汇率、涨价、退款等不作估算。

## 发布到 GitHub

可以把此目录作为独立仓库根目录发布。创建公开仓库 `hold-my-wallet` 后，将目录内容推送到仓库根目录；不要把含个人账单或合同的原始文件提交到仓库。

## 许可

本 Skill 采用 MIT License，详见 `LICENSE`。
