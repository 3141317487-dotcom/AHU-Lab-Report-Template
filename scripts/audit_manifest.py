"""辅助核对已提取的要求，不替代人工读取原要求。仅使用Python标准库。"""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def audit(manifest, report, report_dir):
    findings = []
    requirements = manifest.get('requirements', [])
    if not requirements:
        findings.append('未提供要求清单，不能声称要求核对完成')
    seen = set()
    for r in requirements:
        key = r.get('id', '')
        if not key or key in seen:
            findings.append(f'要求ID缺失或重复：{key}')
        seen.add(key)
        if not r.get('source') or not r.get('quote'):
            findings.append(f'{key}缺少原要求或出处')
        status = r.get('status')
        if status == 'excluded':
            if not r.get('reason'):
                findings.append(f'{key}排除项目缺少原因')
        elif status == 'covered':
            evidence = r.get('evidence', '')
            if not evidence or evidence not in report:
                findings.append(f'{key}交付内容锚点不存在')
        else:
            findings.append(f'{key}未覆盖或状态未知：{status}')
    for i, t in enumerate(manifest.get('source_tables', []), 1):
        if t.replace('\r\n', '\n') not in report.replace('\r\n', '\n'):
            findings.append(f'原表{i}与成品不一致')
    for text in manifest.get('forbidden_text', []):
        if text in report:
            findings.append(f'出现禁止内容：{text}')
    for ref in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', report):
        ref = ref.strip().strip('<>')
        parsed = urlsplit(ref)
        if parsed.scheme:
            # 只验证本地相对图片；远程资源仍需人工检查。
            if parsed.scheme != 'file':
                continue
            ref = unquote(parsed.path)
        else:
            ref = unquote(parsed.path)
        path = Path(ref)
        if not path.is_absolute():
            path = report_dir / path
        if not path.is_file():
            findings.append(f'本地图片不存在：{ref}')
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    findings = audit(json.loads(args.manifest.read_text(encoding='utf-8')),
                     args.report.read_text(encoding='utf-8'), args.report.parent)
    print(json.dumps({'passed': not findings, 'findings': findings,
                      'scope': '仅核对已声明清单；原要求完整性、理论、图像内容和教材正文需人工核实'},
                     ensure_ascii=False, indent=2))
    raise SystemExit(bool(findings))


if __name__ == '__main__':
    main()
