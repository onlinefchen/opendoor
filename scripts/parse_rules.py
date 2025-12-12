#!/usr/bin/env python3
"""
Parse surge.conf and extract rules into separate category files.
"""

import re
import os
from collections import defaultdict

def parse_surge_conf(conf_path):
    """Parse surge.conf and extract rules by category."""
    rules = defaultdict(list)

    with open(conf_path, 'r', encoding='utf-8') as f:
        in_rule_section = False
        for line in f:
            line = line.strip()

            # Check if we're entering the [Rule] section
            if line == '[Rule]':
                in_rule_section = True
                continue

            # Check if we've left the [Rule] section
            if in_rule_section and line.startswith('['):
                break

            if not in_rule_section or not line or line.startswith('#'):
                continue

            # Parse rule line
            parts = line.split(',')
            if len(parts) >= 2:
                rule_type = parts[0]

                # Handle different rule formats
                if rule_type in ['DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'IP-CIDR', 'IP-CIDR6']:
                    if len(parts) >= 3:
                        value = parts[1]
                        category = parts[2]
                        # Build the rule without category (for .list format)
                        if len(parts) > 3:
                            rule_line = f"{rule_type},{value},{','.join(parts[3:])}"
                        else:
                            rule_line = f"{rule_type},{value}"
                        rules[category].append(rule_line)
                elif rule_type == 'GEOIP':
                    if len(parts) >= 3:
                        value = parts[1]
                        category = parts[2]
                        rule_line = f"{rule_type},{value}"
                        rules[category].append(rule_line)
                elif rule_type == 'FINAL':
                    if len(parts) >= 2:
                        category = parts[1]
                        rules[category].append(f"{rule_type}")

    return rules

def category_to_filename(category):
    """Convert category name to filename."""
    # Remove emoji and clean up
    name_map = {
        '📲 电报消息': 'telegram',
        '📹 油管视频': 'youtube',
        '🎥 奈飞视频': 'netflix',
        '🎥 迪士尼+': 'disney',
        '📺 巴哈姆特': 'bahamut',
        '📺 哔哩哔哩': 'bilibili',
        '📢 谷歌FCM': 'google_fcm',
        'Ⓜ️ 微软云盘': 'microsoft_onedrive',
        'Ⓜ️ 微软服务': 'microsoft',
        '🍎 苹果服务': 'apple',
        '🎮 游戏平台': 'game',
        '🎶 网易音乐': 'netease_music',
        '☁️ CloudFlare': 'cloudflare',
        '🤖 ChatGPT': 'chatgpt',
        '📹 TikTok': 'tiktok',
        '🤖 Claude': 'claude',
        '🤖 Gemini': 'gemini',
        '🎮 Steam下载': 'steam_download',
        '🎮 Steam网页': 'steam_web',
        '🤖 Copilot': 'copilot',
        '🎯 全球直连': 'direct',
        ' 🎯 全球直连': 'direct',
        '🐟 漏网之鱼': 'final',
        '🚀 节点选择': 'proxy',
        'REJECT': 'reject',
    }

    return name_map.get(category, category.replace(' ', '_').replace('/', '_'))

def save_rules(rules, output_dir):
    """Save rules to separate files."""
    os.makedirs(output_dir, exist_ok=True)

    for category, rule_list in rules.items():
        if not rule_list:
            continue

        filename = category_to_filename(category)
        if not filename:
            continue

        filepath = os.path.join(output_dir, f"{filename}.list")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {category}\n")
            f.write(f"# Total rules: {len(rule_list)}\n\n")
            for rule in rule_list:
                f.write(rule + '\n')

        print(f"Created {filepath} with {len(rule_list)} rules")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    conf_path = os.path.join(project_dir, 'surge.conf')
    output_dir = os.path.join(project_dir, 'surge_rule')

    print(f"Parsing {conf_path}...")
    rules = parse_surge_conf(conf_path)

    print(f"\nFound {len(rules)} categories:")
    for category in sorted(rules.keys()):
        print(f"  - {category}: {len(rules[category])} rules")

    print(f"\nSaving rules to {output_dir}...")
    save_rules(rules, output_dir)

    print("\nDone!")

if __name__ == '__main__':
    main()
