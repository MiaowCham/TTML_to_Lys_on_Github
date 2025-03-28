import os
import re
import string
import logging
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime
import base64
from github import Github

from pip import main as pip_main

# install loguru and import
try:
    import loguru
except ImportError:
    pip_main(['install', 'loguru'])
    import loguru

finally:
    from loguru import logger

namespaces = {
    'tt': 'http://www.w3.org/ns/ttml',
    'ttm': 'http://www.w3.org/ns/ttml#metadata',
    'amll': 'http://www.example.com/ns/amll',
    'itunes': 'http://music.apple.com/lyric-ttml-internal'
}

# 设置日志
logger.add(sys.stderr, level='INFO')

def preprocess_ttml(content):
    """预处理TTML内容，移除xmlns=""声明"""
    pattern = re.compile(r'\s+xmlns=""')
    modified = False
    matches = pattern.findall(content)
    if matches:
        modified = True
        content = pattern.sub('', content)
        logger.info(f"发现并移除了 {len(matches)} 处xmlns=\"\"声明")
    return content, modified, matches

def preprocess_ttml_1(content):
    """预处理TTML内容，移除过多括号"""
    pattern = re.compile(r'([()])1+')
    modified = False
    matches = pattern.findall(content)
    if matches:
        modified = True
        content = pattern.sub(r'\1', content)
        logger.info(f"发现并移除了 {len(matches)} 处连续括号")
    return content, modified, matches

def parse_time(time_str):
    """将时间字符串转换为毫秒"""
    try:
        parts = time_str.replace(',', '.').split(':')
        if len(parts) == 3:  # hh:mm:ss.ms
            h, m, rest = parts
            s, ms = rest.split('.') if '.' in rest else (rest, 0)
        elif len(parts) == 2:  # mm:ss.ms
            m, rest = parts
            h = 0
            s, ms = rest.split('.') if '.' in rest else (rest, 0)
        else:  # ss.ms
            h, m = 0, 0
            s, ms = parts[0].split('.') if '.' in parts[0] else (parts[0], 0)

        return (int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 +
                int(str(ms).ljust(3, '0')[:3]))
    except Exception as e:
        logger.error(f"时间解析错误: {time_str} - {str(e)}")
        return 0

def format_lrc_time(millis):
    """将毫秒转换为LRC时间格式 (mm:ss.xx)"""
    millis = max(0, millis)
    m = millis // 60000
    s = (millis % 60000) // 1000
    ms = millis % 1000
    return f"{m:02d}:{s:02d}.{ms:03d}"

def calculate_property(alignment, background):
    """计算LYS属性值"""
    if background:
        return {None: 6, 'left': 7, 'right': 8}.get(alignment, 6)
    else:
        return {None: 3, 'left': 4, 'right': 5}.get(alignment, 3)

def process_segment(spans, alignment, is_background):
    """处理歌词段生成LYS行（最终空格修复版）"""
    parts = []
    pending_whitespace = ''

    for span in spans:
        try:
            begin = span.get('begin')
            end = span.get('end')
            if not begin or not end:
                continue

            start = parse_time(begin)
            duration = parse_time(end) - start
            if duration <= 0:
                continue

            full_text = pending_whitespace + (span.text or '')
            clean_text = full_text.rstrip(' ')
            trailing_spaces = len(full_text) - len(clean_text)

            tail = span.tail or ''
            tail_clean = tail.lstrip(' ')
            leading_spaces = len(tail) - len(tail_clean)

            word = clean_text
            if trailing_spaces > 0 or leading_spaces > 0:
                word += ' ' * (trailing_spaces + leading_spaces)

            if word:
                parts.append(f"{word}({start},{duration})")

            pending_whitespace = tail_clean if not tail_clean.strip() else ''

        except Exception as e:
            logger.warning(f"处理span失败: {str(e)}")

    if pending_whitespace.strip():
        parts.append(f"{pending_whitespace}(0,0)")

    if not parts:
        return None

    prop = calculate_property(alignment, is_background)
    return f"[{prop}]" + "".join(parts)

def process_translations(p_element):
    """处理翻译内容"""
    translations = []
    for elem in p_element.iter():
        if elem.tag == f'{{{namespaces["tt"]}}}span':
            role = elem.get(f'{{{namespaces["ttm"]}}}role')
            if role == 'x-translation':
                text = (elem.text or '').strip()
                if text:
                    translations.append(text)
    return ' '.join(translations)

def ttml_to_lys(ttml_content):
    """主转换函数"""
    try:
        # 预处理移除xmlns=""声明
        pro_processed_content, modified, matches = preprocess_ttml(ttml_content)
        revise_1 = modified

        # 预处理移除多余括号
        processed_content, modified_1, matches1 = preprocess_ttml_1(pro_processed_content)
        revise_2 = modified_1

        # 解析XML
        root = ET.fromstring(processed_content)

    except Exception as e:
        logger.exception("无法解析TTML内容")
        return None

    lys_lines = []
    lrc_entries = []
    has_translations = False

    # 处理歌词行
    try:
        for p in root.findall('.//tt:p', namespaces):
            try:
                # 获取基础信息
                alignment = None
                agent = p.get(f'{{{namespaces["ttm"]}}}agent')
                if agent == 'v1':
                    alignment = 'left'
                elif agent == 'v2':
                    alignment = 'right'

                # 处理翻译
                translation = process_translations(p)
                if translation:
                    has_translations = True

                # 获取时间信息
                p_begin = p.get('begin')
                lrc_time = format_lrc_time(parse_time(p_begin))
                lrc_entries.append((lrc_time, translation))

                # 分离主歌词和背景人声
                main_spans = []
                bg_spans = []

                def analyse_line(line: ET.Element, is_bg: bool):
                    for word in line:
                        word_role = word.get(f'{{{namespaces["ttm"]}}}role')
                        if word_role == 'x-bg':
                            analyse_line(word, True)
                        else:
                            if is_bg:
                                bg_spans.append(word)
                            else:
                                main_spans.append(word)

                analyse_line(p, False)

                # 处理主歌词行
                if main_spans:
                    main_line = process_segment(main_spans, alignment, False)
                    if main_line:
                        lys_lines.append(main_line)

                # 处理背景人声行
                if bg_spans:
                    bg_line = process_segment(bg_spans, alignment, True)
                    if bg_line:
                        lys_lines.append(bg_line)

            except Exception as e:
                logger.exception("处理歌词行失败")

    except Exception as e:
        logger.exception("解析歌词失败")
        return None

    result = {
        'lys_content': '\n'.join(lys_lines),
        'has_translations': has_translations,
        'lrc_content': '\n'.join([f"[{time}]{text}" for time, text in lrc_entries]) if has_translations else None,
        'revisions': {
            'xmlns_removed': revise_1,
            'brackets_fixed': revise_2,
            'xmlns_matches': len(matches) if matches else 0,
            'bracket_matches': len(matches1) if matches1 else 0
        }
    }

    return result

def process_issue():
    """处理GitHub Issue"""
    try:
        # 获取环境变量
        github_token = os.environ['GITHUB_TOKEN']
        repo_name = os.environ['GITHUB_REPOSITORY']
        issue_number = int(os.environ['ISSUE_NUMBER'])

        # 初始化GitHub客户端
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(issue_number)

        # 获取Issue内容
        body = issue.body
        if not body:
            issue.create_comment("❌ Issue内容为空，请提供TTML内容")
            return

        # 处理TTML内容
        result = ttml_to_lys(body)
        if not result:
            issue.create_comment("❌ TTML处理失败，请检查内容格式是否正确")
            return

        # 准备评论内容
        comment = ["✅ 转换完成！"]

        # 添加LYS文件
        comment.append("\n### LYS文件内容")
        comment.append("```")
        comment.append(result['lys_content'])
        comment.append("```")

        # 如果有翻译，添加LRC文件
        if result['has_translations']:
            comment.append("\n### 翻译文件内容")
            comment.append("```")
            comment.append(result['lrc_content'])
            comment.append("```")

        # 添加处理信息
        if result['revisions']['xmlns_removed']:
            comment.append(f"\n处理文件时移除了 {result['revisions']['xmlns_matches']} 处xmlns=\"\"声明")
        if result['revisions']['brackets_fixed']:
            comment.append(f"处理文件时移除了 {result['revisions']['bracket_matches']} 处多余的括号")

        # 发布评论
        issue.create_comment('\n'.join(comment))

    except Exception as e:
        logger.exception("处理Issue时发生错误")
        if 'issue' in locals():
            issue.create_comment(f"❌ 处理过程中发生错误：{str(e)}")

if __name__ == '__main__':
    process_issue()
