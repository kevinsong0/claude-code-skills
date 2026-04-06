#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 转 Q&A 格式处理器（使用 AI 模型）

通过调用大模型接口将 Markdown 文件转换为高质量问答格式。
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 设置默认编码为 UTF-8，避免中文编码问题
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


API_KEY = os.getenv("XAI_API_KEY") or os.getenv("OPENAI_API_KEY")
API_URL = "https://api.xairouter.com/v1/chat/completions"
MODEL = "glm-4.7"


def get_default_target_dir() -> str:
    """
    获取适配操作系统的默认目标目录路径

    Returns:
        str: 默认目标目录路径
    """
    return r"C:\Users\sksua\Nutstore\1\Obsidian (1)\Q&A"


def call_ai_api(content: str, retry_count: int = 3, delay: float = 1.0) -> str:
    """
    调用 AI API 将内容转换为 Q&A 格式

    Args:
        content: 原始内容
        retry_count: 重试次数
        delay: 重试延迟（秒）

    Returns:
        str: 转换后的 Q&A 内容
    """
    if not API_KEY:
        raise EnvironmentError("未设置 API Key，请配置 XAI_API_KEY 或 OPENAI_API_KEY")

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的知识整理助手。请将用户提供的内容整理为问答的形式，尽量详细。确保问题清晰准确，回答全面深入，保持原文的语义和逻辑。输出格式：问题在前，回答在后，问题使用 '### Q:' 前缀，回答使用 'A:' 前缀。",
            },
            {"role": "user", "content": f"整理为问答的形式，尽量详细：\n\n{content}"},
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
    }

    for attempt in range(retry_count):
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=60)

            if response.status_code == 200:
                result = response.json()

                if "choices" in result and len(result["choices"]) > 0:
                    ai_content = result["choices"][0]["message"]["content"]
                    return ai_content
                else:
                    raise ValueError(f"API 返回格式错误: {result}")
            else:
                error_msg = (
                    f"API 请求失败 (状态码: {response.status_code}): {response.text}"
                )
                if attempt < retry_count - 1:
                    print(
                        f"重试 {attempt + 1}/{retry_count}: {error_msg}",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise ValueError(error_msg)

        except requests.exceptions.Timeout:
            error_msg = "API 请求超时"
            if attempt < retry_count - 1:
                print(f"重试 {attempt + 1}/{retry_count}: {error_msg}", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
            else:
                raise TimeoutError(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求错误: {str(e)}"
            if attempt < retry_count - 1:
                print(f"重试 {attempt + 1}/{retry_count}: {error_msg}", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
            else:
                raise ConnectionError(error_msg)

    raise RuntimeError("AI API 调用失败")


def format_qa_output(ai_content: str) -> str:
    """
    格式化 AI 输出为标准 Q&A 格式

    Args:
        ai_content: AI 返回的内容

    Returns:
        str: 格式化后的 Q&A 内容
    """
    lines = ai_content.strip().split("\n")
    formatted_lines = []
    current_section = None

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if formatted_lines:
                formatted_lines.append("")
            continue

        is_question = (
            stripped.lower().startswith("q:")
            or stripped.lower().startswith("问题")
            or stripped.lower().startswith("### q:")
            or stripped.lower().startswith("### 问题")
        )

        is_answer = (
            stripped.lower().startswith("a:")
            or stripped.lower().startswith("回答")
            or stripped.lower().startswith("### a:")
            or stripped.lower().startswith("### 回答")
        )

        if is_question:
            if current_section == "A":
                formatted_lines.append("")
            current_section = "Q"
            question = (
                stripped.replace("### Q:", "")
                .replace("### q:", "")
                .replace("### 问题：", "")
                .replace("### 问题:", "")
                .replace("Q:", "")
                .replace("q:", "")
                .replace("问题：", "")
                .replace("问题:", "")
                .strip()
            )
            formatted_lines.append(f"### Q: {question}")
        elif is_answer:
            if current_section == "Q":
                formatted_lines.append("")
            current_section = "A"
            answer = (
                stripped.replace("### A:", "")
                .replace("### a:", "")
                .replace("### 回答：", "")
                .replace("### 回答:", "")
                .replace("A:", "")
                .replace("a:", "")
                .replace("回答：", "")
                .replace("回答:", "")
                .strip()
            )
            formatted_lines.append(f"A: {answer}")
        else:
            has_wiki_link = ("[[" in line and "]]" in line) or (
                "! [[" in line.replace(" ", "") and "]]" in line
            )

            if has_wiki_link or current_section == "A":
                formatted_lines.append(line)
            elif current_section == "Q" or not current_section:
                if not any(
                    l.lower().startswith(
                        (
                            "q:",
                            "a:",
                            "问题",
                            "回答",
                            "### q:",
                            "### a:",
                            "### 问题",
                            "### 回答",
                        )
                    )
                    for l in formatted_lines[-5:]
                    if formatted_lines
                ):
                    if stripped and not stripped.startswith(
                        (
                            "-",
                            "*",
                            "+",
                            "1.",
                            "2.",
                            "3.",
                            "4.",
                            "5.",
                            "6.",
                            "7.",
                            "8.",
                            "9.",
                        )
                    ):
                        if not formatted_lines[-1].strip() if formatted_lines else True:
                            formatted_lines.append(f"### Q: {stripped}")
                        else:
                            formatted_lines[-1] += f" {stripped}"
                    else:
                        formatted_lines.append(line)
                else:
                    formatted_lines.append(line)
            else:
                if formatted_lines:
                    formatted_lines.append(line)

    if not formatted_lines:
        return ai_content

    return "\n".join(formatted_lines)


def process_single_file(
    filepath: Path,
    target_dir: Path,
    preserve_original: bool,
    file_index: int,
    total_files: int,
) -> Dict[str, Any]:
    """
    处理单个 Markdown 文件

    Args:
        filepath: 文件路径
        target_dir: 目标目录
        preserve_original: 是否保留原文
        file_index: 文件索引
        total_files: 文件总数

    Returns:
        Dict: 处理结果
    """
    result = {
        "filepath": str(filepath),
        "success": False,
        "error": None,
        "original_size": 0,
        "qa_size": 0,
    }

    try:
        print(f"[{file_index}/{total_files}] 处理: {filepath.name}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        result["original_size"] = len(content)

        if not content.strip():
            result["error"] = "文件内容为空"
            return result

        print(f"[{file_index}/{total_files}] 调用 AI API 处理...")
        ai_content = call_ai_api(content)

        print(f"[{file_index}/{total_files}] 格式化输出...")
        qa_content = format_qa_output(ai_content)

        if not qa_content.strip():
            result["error"] = "AI 返回内容为空"
            return result

        result["qa_size"] = len(qa_content)

        if preserve_original:
            qa_filepath = filepath.parent / f"{filepath.stem}_QA{filepath.suffix}"
        else:
            qa_filepath = filepath

        with open(qa_filepath, "w", encoding="utf-8") as f:
            f.write(qa_content)

        if not preserve_original:
            archive_dir = target_dir / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)

            target_filepath = archive_dir / filepath.name
            counter = 1
            while target_filepath.exists():
                new_name = f"{filepath.stem}_{counter}{filepath.suffix}"
                target_filepath = archive_dir / new_name
                counter += 1

            os.replace(str(filepath), str(target_filepath))

        result["success"] = True
        print(f"[{file_index}/{total_files}] ✓ 完成: {filepath.name}")

    except UnicodeDecodeError as e:
        result["error"] = f"文件编码错误: {str(e)}"
        print(
            f"[{file_index}/{total_files}] ✗ 失败: {filepath.name} - {result['error']}",
            file=sys.stderr,
        )
    except Exception as e:
        result["error"] = str(e)
        print(
            f"[{file_index}/{total_files}] ✗ 失败: {filepath.name} - {result['error']}",
            file=sys.stderr,
        )

    return result


def is_markdown_file(filepath: Path) -> bool:
    """
    检查是否为 Markdown 文件

    Args:
        filepath: 文件路径

    Returns:
        bool: 是否为 Markdown 文件
    """
    return filepath.suffix.lower() in [".md", ".markdown"]


def refine_markdown_to_qa(
    source_dir: str,
    target_dir: Optional[str] = None,
    preserve_original: bool = True,
    max_workers: int = 3,
) -> Dict[str, Any]:
    """
    将源目录中的所有 Markdown 文件通过 AI 转换为 Q&A 格式

    Args:
        source_dir: 源目录路径
        target_dir: 目标目录路径（可选）
        preserve_original: 是否保留原始文件副本
        max_workers: 最大并发数（默认 1，避免 API 限流）

    Returns:
        Dict: 处理结果
    """
    source_path = Path(source_dir)

    if not source_path.exists():
        return {
            "success": [],
            "failed": {source_dir: "源目录不存在"},
            "stats": {
                "total": 0,
                "success": 0,
                "failed": 0,
                "total_original_size": 0,
                "total_qa_size": 0,
            },
        }

    if target_dir is None:
        target_dir = get_default_target_dir()

    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    md_files = sorted(
        [f for f in source_path.iterdir() if f.is_file() and is_markdown_file(f)]
    )

    if not md_files:
        print(f"警告: 目录中没有找到 Markdown 文件")
        return {
            "success": [],
            "failed": {},
            "stats": {
                "total": 0,
                "success": 0,
                "failed": 0,
                "total_original_size": 0,
                "total_qa_size": 0,
            },
        }

    print(f"找到 {len(md_files)} 个 Markdown 文件")
    print(f"源目录: {source_path}")
    print(f"目标目录: {target_path}")
    print(f"保留原文: {preserve_original}")
    print(f"并发数: {max_workers}")
    print("=" * (60 if sys.stdout.encoding != "gbk" else 30))

    results = []

    if max_workers == 1:
        for idx, filepath in enumerate(md_files, 1):
            result = process_single_file(
                filepath, target_path, preserve_original, idx, len(md_files)
            )
            results.append(result)
            time.sleep(2)
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    process_single_file,
                    filepath,
                    target_path,
                    preserve_original,
                    idx,
                    len(md_files),
                ): filepath
                for idx, filepath in enumerate(md_files, 1)
            }

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

    success_files = [r["filepath"] for r in results if r["success"]]
    failed_files = {r["filepath"]: r["error"] for r in results if not r["success"]}

    total_original_size = sum(r["original_size"] for r in results)
    total_qa_size = sum(r["qa_size"] for r in results if r["success"])

    print("=" * (60 if sys.stdout.encoding != "gbk" else 30))
    print(f"处理完成:")
    print(f"  成功: {len(success_files)} 个文件")
    print(f"  失败: {len(failed_files)} 个文件")
    print(f"  原文总大小: {total_original_size} 字节")
    print(f"  Q&A 总大小: {total_qa_size} 字节")

    if failed_files:
        print("\n失败文件列表:")
        for filepath, error in failed_files.items():
            print(f"  - {Path(filepath).name}: {error}")

    return {
        "success": success_files,
        "failed": failed_files,
        "stats": {
            "total": len(md_files),
            "success": len(success_files),
            "failed": len(failed_files),
            "total_original_size": total_original_size,
            "total_qa_size": total_qa_size,
        },
    }


def main():
    """命令行入口函数"""
    if len(sys.argv) < 2:
        print(
            "用法: python refine_markdown_to_qa.py <source_dir> [target_dir] [preserve_original] [max_workers]"
        )
        print()
        print("参数:")
        print("  source_dir        源目录路径（必需）")
        print(
            "  target_dir        目标目录（可选，默认: C:\\Users\\sksua\\Nutstore\\1\\Obsidian (1)\\Q&A）"
        )
        print("  preserve_original 是否保留原文（可选，默认: Flase）")
        print("  max_workers       最大并发数（可选，默认: 3）")
        print()
        print("示例:")
        print("  python refine_markdown_to_qa.py C:/notes")
        print("  python refine_markdown_to_qa.py C:/notes C:/qa True")
        print("  python refine_markdown_to_qa.py C:/notes C:/qa False 3")
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else None
    preserve_original = sys.argv[3].lower() != "false" if len(sys.argv) > 3 else True
    max_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 3

    result = refine_markdown_to_qa(
        source_dir, target_dir, preserve_original, max_workers
    )

    sys.exit(0 if len(result["failed"]) == 0 else 1)


if __name__ == "__main__":
    main()
