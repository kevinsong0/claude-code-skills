from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_VAULT_ROOT = Path(r"D:\Nutstore\Obsidian")
DEFAULT_RAW_SOURCE = Path(r"D:\Nutstore\Obsidian")
DEFAULT_ENGINE_ROOT = Path(r"D:\Nutstore\Obsidian\Coding\obsidian-kb-engine")
DEFAULT_PROJECT = "main-wiki"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "qwen/qwen3.6-plus:free"
DEFAULT_PROMPT_VERSION = "2026-04-05-llm-first-v5"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="One-command Obsidian KB internalization pipeline")
    p.add_argument("--project", default=DEFAULT_PROJECT, help="KB project name")
    p.add_argument("--vault-root", default=str(DEFAULT_VAULT_ROOT), help="Vault root path")
    p.add_argument("--raw-source", default=str(DEFAULT_RAW_SOURCE), help="Source raw folder")
    p.add_argument("--engine-root", default=str(DEFAULT_ENGINE_ROOT), help="Path containing kb.py")
    p.add_argument(
        "--all-formats",
        action="store_true",
        help="Ingest all supported formats. Default is Markdown only.",
    )
    p.add_argument("--full-compile", action="store_true", help="Force full compile")
    p.add_argument("--ask", default=None, help="Optional QA question")
    p.add_argument("--render", default=None, help="Optional render question")
    p.add_argument("--skip-health", action="store_true", help="Skip health check")
    p.add_argument("--apply-stale", action="store_true", help="Apply stale-claim updates during health step")
    p.add_argument("--stale-plan-only", action="store_true", help="Generate stale plan only during health step")
    p.add_argument("--apply-stale-from", default=None, help="Apply stale updates from given plan JSON file")
    p.add_argument("--no-backlog", action="store_true", help="Skip backlog/review queue generation in health")
    p.add_argument("--skip-ingest", action="store_true", help="Skip ingest step and compile current project raw/")
    p.add_argument("--skip-compile", action="store_true", help="Skip compile step")
    p.add_argument("--api-key", default=None, help="LLM API key (writes into --api-key-env)")
    p.add_argument("--api-key-env", default="OR_API_KEY", help="Environment variable name for LLM API key")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL, help="OpenAI-compatible base URL")
    p.add_argument("--model", default=DEFAULT_MODEL, help="Model name")
    p.add_argument(
        "--model-pool",
        default=None,
        help="Comma-separated model list for concurrent compile, e.g. 'glm-5,qwen3.5-plus'",
    )
    p.add_argument("--timeout-seconds", type=int, default=180, help="LLM timeout seconds")
    p.add_argument("--summary-max-chars", type=int, default=3600, help="Source context chars for compile")
    p.add_argument("--summary-workers", type=int, default=None, help="Concurrent compile workers")
    p.add_argument("--concepts-per-doc", type=int, default=8, help="Target concepts per source document")
    p.add_argument("--concept-min-source-count", type=int, default=3, help="Min shared sources to keep concept page")
    p.add_argument("--prompt-version", default=DEFAULT_PROMPT_VERSION, help="Compile prompt version tag")
    p.add_argument("--followup", action="store_true", help="Auto answer open questions to outputs/待追问")
    p.add_argument("--followup-max-per-source", type=int, default=3, help="Max pending questions per source")
    p.add_argument("--followup-max-sources", type=int, default=20, help="Max source notes for followup")
    p.add_argument("--followup-top-k", type=int, default=6, help="Retrieved docs per followup question")
    p.add_argument("--concept-define", action="store_true", help="Force concept definition generation by LLM")
    p.add_argument("--skip-concept-define", action="store_true", help="Skip concept definition generation in default pipeline")
    p.add_argument("--concept-define-max", type=int, default=500, help="Max concept notes to define")
    p.add_argument("--concept-define-min-source", type=int, default=2, help="Only define concepts with >= N sources")
    p.add_argument("--concept-define-batch-size", type=int, default=5, help="Concept definitions per LLM batch")
    p.add_argument("--concept-define-overwrite", action="store_true", help="Overwrite existing concept definitions")
    p.add_argument("--qa-top-k", type=int, default=6, help="Retrieved docs per QA question")
    p.add_argument("--qa-context-chars", type=int, default=1200, help="Context chars per retrieved doc")
    p.add_argument("--qa-answer-max-tokens", type=int, default=1200, help="Max output tokens for QA/followup answer")
    return p


def run_step(step: str, cmd: list[str], cwd: Path, env: dict[str, str]) -> None:
    print(f"\n[{step}] {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, env=env)
    if proc.stdout.strip():
        print(proc.stdout.strip())
    if proc.returncode != 0:
        if proc.stderr.strip():
            print(proc.stderr.strip(), file=sys.stderr)
        raise SystemExit(proc.returncode)


def ensure_source_ready(source: Path) -> None:
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"Raw source not found: {source}")
    has_files = any(p.is_file() for p in source.rglob("*"))
    if not has_files:
        raise SystemExit(f"Raw source is empty: {source}")


def update_project_llm_config(
    project_root: Path,
    base_url: str,
    model: str,
    api_key_env: str,
    model_pool: list[str] | None,
    timeout_seconds: int,
    summary_max_chars: int,
    summary_workers: int | None,
    concepts_per_doc: int,
    concept_min_source_count: int,
    prompt_version: str,
    qa_top_k: int,
    qa_context_chars: int,
    qa_answer_max_tokens: int,
) -> None:
    cfg_path = project_root / "project.json"
    if not cfg_path.exists():
        return
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    llm = cfg.setdefault("llm", {})
    llm["base_url"] = base_url
    llm["model"] = model
    if model_pool:
        llm["model_pool"] = model_pool
    else:
        llm.pop("model_pool", None)
    llm["api_key_env"] = api_key_env
    llm["temperature"] = 0.0
    llm["timeout_seconds"] = max(30, int(timeout_seconds))
    compile_cfg = cfg.setdefault("compile", {})
    compile_cfg.pop("concept_mode", None)
    compile_cfg["summary_max_chars"] = max(1200, int(summary_max_chars))
    worker_default = max(4, len(model_pool or [model]))
    compile_cfg["summary_workers"] = max(1, int(summary_workers or worker_default))
    compile_cfg["concepts_per_doc"] = max(4, min(12, int(concepts_per_doc)))
    compile_cfg["concept_min_source_count"] = max(2, int(concept_min_source_count))
    compile_cfg["prompt_version"] = str(prompt_version).strip() or DEFAULT_PROMPT_VERSION
    compile_cfg["use_llm_concept_body"] = False
    compile_cfg["preserve_existing_concept_definition"] = True
    compile_cfg["quality_first_pool"] = True
    qa_cfg = cfg.setdefault("qa", {})
    qa_cfg["top_k"] = max(3, int(qa_top_k))
    qa_cfg["context_chars_per_doc"] = max(600, int(qa_context_chars))
    qa_cfg["answer_max_tokens"] = max(400, int(qa_answer_max_tokens))
    qa_cfg["writeback_to_wiki"] = True
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()

    vault_root = Path(args.vault_root).expanduser().resolve()
    raw_source = Path(args.raw_source).expanduser().resolve()
    engine_root = Path(args.engine_root).expanduser().resolve()
    kb_cli = engine_root / "kb.py"

    if not kb_cli.exists():
        raise SystemExit(f"kb.py not found: {kb_cli}")

    ensure_source_ready(raw_source)

    py = sys.executable
    project = args.project
    env = os.environ.copy()
    api_key_env = str(args.api_key_env).strip() or "OR_API_KEY"
    if args.api_key:
        env[api_key_env] = args.api_key
    if api_key_env not in env or not env[api_key_env].strip():
        raise SystemExit(f"{api_key_env} missing. Set env var or pass --api-key.")
    model_pool = None
    if args.model_pool:
        model_pool = [m.strip() for m in str(args.model_pool).split(",") if m.strip()]
        if not model_pool:
            model_pool = None

    run_step(
        "init",
        [py, str(kb_cli), "init", project, "--vault-root", str(vault_root)],
        cwd=engine_root,
        env=env,
    )
    update_project_llm_config(
        project_root=vault_root / project,
        base_url=args.base_url,
        model=args.model,
        api_key_env=api_key_env,
        model_pool=model_pool,
        timeout_seconds=args.timeout_seconds,
        summary_max_chars=args.summary_max_chars,
        summary_workers=args.summary_workers,
        concepts_per_doc=args.concepts_per_doc,
        concept_min_source_count=args.concept_min_source_count,
        prompt_version=args.prompt_version,
        qa_top_k=args.qa_top_k,
        qa_context_chars=args.qa_context_chars,
        qa_answer_max_tokens=args.qa_answer_max_tokens,
    )
    project_raw_dir = (vault_root / project / "raw").resolve()
    auto_skip_ingest = raw_source == project_raw_dir
    if args.skip_ingest or auto_skip_ingest:
        reason = "--skip-ingest" if args.skip_ingest else "raw-source points to project raw/"
        print(f"\n[ingest] skipped ({reason})")
    else:
        run_step(
            "ingest",
            [
                py,
                str(kb_cli),
                "ingest",
                project,
                "--source",
                str(raw_source),
                *([] if args.all_formats else ["--md-only"]),
                "--vault-root",
                str(vault_root),
            ],
            cwd=engine_root,
            env=env,
        )

    if args.skip_compile:
        print("\n[compile] skipped (--skip-compile)")
    else:
        compile_cmd = [py, str(kb_cli), "compile", project, "--vault-root", str(vault_root)]
        if args.full_compile:
            compile_cmd.append("--full")
        run_step("compile", compile_cmd, cwd=engine_root, env=env)

    should_run_conceptdef = (not args.skip_compile and not args.skip_concept_define) or args.concept_define
    if should_run_conceptdef:
        cmd = [
            py,
            str(kb_cli),
            "conceptdef",
            project,
            "--max-concepts",
            str(max(1, args.concept_define_max)),
            "--min-source-count",
            str(max(1, args.concept_define_min_source)),
            "--batch-size",
            str(max(1, min(10, args.concept_define_batch_size))),
            "--vault-root",
            str(vault_root),
        ]
        if args.concept_define_overwrite:
            cmd.append("--overwrite")
        run_step("conceptdef", cmd, cwd=engine_root, env=env)
    else:
        reason = "--skip-concept-define" if args.skip_concept_define else "compile skipped and no --concept-define"
        print(f"\n[conceptdef] skipped ({reason})")

    if not args.skip_health:
        health_cmd = [py, str(kb_cli), "health", project, "--vault-root", str(vault_root)]
        if args.stale_plan_only:
            health_cmd.append("--stale-plan-only")
        if args.apply_stale_from:
            health_cmd.extend(["--apply-stale-from", str(args.apply_stale_from)])
        if args.apply_stale:
            health_cmd.append("--apply-stale")
        if args.no_backlog:
            health_cmd.append("--no-backlog")
        run_step(
            "health",
            health_cmd,
            cwd=engine_root,
            env=env,
        )

    if args.ask:
        run_step(
            "ask",
            [
                py,
                str(kb_cli),
                "ask",
                project,
                "--question",
                args.ask,
                "--vault-root",
                str(vault_root),
            ],
            cwd=engine_root,
            env=env,
        )

    if args.render:
        run_step(
            "render",
            [
                py,
                str(kb_cli),
                "render",
                project,
                "--question",
                args.render,
                "--vault-root",
                str(vault_root),
            ],
            cwd=engine_root,
            env=env,
        )

    if args.followup:
        run_step(
            "followup",
            [
                py,
                str(kb_cli),
                "followup",
                project,
                "--max-per-source",
                str(max(1, args.followup_max_per_source)),
                "--max-sources",
                str(max(1, args.followup_max_sources)),
                "--top-k",
                str(max(3, args.followup_top_k)),
                "--vault-root",
                str(vault_root),
            ],
            cwd=engine_root,
            env=env,
        )

    project_root = vault_root / project
    print("\n[done]")
    print(f"Project root: {project_root}")
    print(f"Wiki index: {project_root / 'wiki' / 'Wiki-Index.md'}")
    print(f"Outputs: {project_root / 'outputs'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
