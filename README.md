# 安大实验报告模板

一个按教师要求编写实验报告的中文 AI skill：让该做的有据可查，让没要求的测量不进入报告。

适用于根据PPT、实验指导书、报告册照片制作Markdown实验报告，补充必要计算、参考波形与待填位置，并逐条对照原要求。适用于Codex等支持`SKILL.md`的助手。

本项目为个人开源工具，不是安徽大学官方模板，不代表学校或教师认可。

## 核心规则

- 五个报告主栏目固定，按下面的模板填写，不自行增删改名；有思考题时放在“分析与讨论”最后。
- 原表怎么写就怎么保留，包括行列、`DC offset`、`1KHz`等具体写法。
- 区分观察、测量、记录、画图和计算；“观察四种、任选一种画图”不能扩展为四组参数逐项实测表。
- 明确“不做”的项目不安排实施，不虚构结果。
- 理论值、参考图与实测值分清；用户要求红色参考时整块显著突出。
- 没测的数据留空，没有读到指定教材正文就不编教材出处。
- 先按原要求逐项找交付内容，再从成品反查每个测量栏的依据。

## 固定报告栏目

报告采用用户提供的报告册结构，五个主栏目和顺序写死：

1. 实验目的
2. 实验器材
3. 实验原理或相关知识
4. 实验或程序运行结果、数据记录
5. 分析与讨论

模板文件：[assets/report-template.md](assets/report-template.md)。具体实验内容依课件要求填写，模板不预设测量项目。思考题属于第五部分的最后一个小节，不单独增加第六部分；没有思考题时不凭空添加。

## 安装

最方便的方式：**直接把本仓库地址发给AI，让AI下载并安装即可。** 适用于能访问网络、下载文件并安装skill的AI助手。可以直接复制下面这段话：

```text
请下载这个仓库，并将其中的skill安装到你使用的技能目录：
https://github.com/3141317487-dotcom/AHU-Lab-Report-Template
安装后读取SKILL.md，后续按这个skill帮我写实验报告。
```

已安装后想更新，也可以直接告诉AI：“请从这个仓库更新安大实验报告模板skill。”

### 手动安装

将本仓库克隆到助手的skills目录，或复制整个仓库为一个skill文件夹。

```sh
git clone https://github.com/3141317487-dotcom/AHU-Lab-Report-Template.git ~/.agents/skills/ahu-lab-report-template
```

Codex也可放到你的`~/.codex/skills/ahu-lab-report-template/`。让助手重新发现技能后使用。具体加载方式以所用客户端为准。

## 使用示例

```text
使用 ahu-lab-report-template，根据这份PPT和实验报告册写Markdown。
只做PPT要求的项目。实测数据留空，参考数值用红色。
原表保持不变，空白作图纸和红框参考图都放同一正文。
思考题放在分析与讨论最后，交付前逐条核对原要求。
```

请提供可读取的课件和报告格式。若方法必须来自某本教材，应提供准确书名版次或可读正文。书目页面不能替代方法所在页。

## 文件结构

```text
SKILL.md                       技能说明
assets/report-template.md      固定五部分的报告模板
references/final-checklist.md   人工交付核对清单
scripts/audit_manifest.py       原表、内容覆盖与图片链接检查
evals/evals.json                合成测试提示
LICENSE                        MIT许可证
```

## 私有核对清单与自动检查

将任务要求清单留在工作目录，不放进提交正文。示例结构：

```json
{
  "requirements": [
    {"id": "r1", "source": "PPT第8页", "quote": "计算各组时间常数", "status": "covered", "evidence": "理论时间常数"}
  ],
  "source_tables": ["| 序号 | 1 | 2 |\n|---|---|---|\n| R | 10K | 20K |"],
  "forbidden_text": ["新增实测电源内阻"]
}
```

```sh
python scripts/audit_manifest.py requirements.json report.md
```

检查会验证声明的必做项目有文字锚点、原表按文本保留、禁止项目不存在，以及本地Markdown图片文件存在。**这是辅助检查，不能发现你在清单里漏掉的教师要求，不能验证图像内容、计算正确性或教材出处。** 仍需按`references/final-checklist.md`逐项人工对照。

`evals/evals.json`使用合成材料，覆盖任选范围、原表写法、教材证据不足三类回归问题。已进行一轮有skill/无skill的独立合成小样本检查，两组均通过这三项场景的检查。这说明用例范围内未复现问题，不证明skill优于基线，也不替代真实课件审阅。辅助脚本与固定栏目模板另有7项单元测试。

## 开源范围

仅包含通用流程与合成测试。原始课件、学生报告、个人资料、教材扫描件、聊天截图和账号凭据不随项目分发。

MIT许可，见[LICENSE](LICENSE)。
