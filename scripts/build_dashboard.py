#!/usr/bin/env python3
"""Build plots and dashboard markdown from public CSV inputs."""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets" / "plots"
DASHBOARD_DIR = ROOT / "dashboard"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]


def parse_float(value: str) -> float:
    return float(value)


def parse_int(value: str) -> int:
    return int(float(value))


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    header_line = "| " + " | ".join(headers) + " |"
    divider_line = "|" + "|".join([" --- " for _ in headers]) + "|"
    body_lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, divider_line] + body_lines)


def format_yes_no(value: str) -> str:
    return "Yes" if str(value).strip().lower() == "yes" else "No"


def build_ok_rate_plot(rows: list[dict[str, str]], output: Path) -> None:
    fig, ax = plt.subplots()
    iters = [parse_int(row["iter"]) for row in rows]
    ok_rates = [parse_float(row["ok_rate"]) for row in rows]
    ax.plot(iters, ok_rates, marker="o")
    ax.set_title("Overall OK Rate")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("OK Rate")
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def build_mix_plot(rows: list[dict[str, str]], output: Path) -> None:
    fig, ax = plt.subplots()
    iters = [parse_int(row["iter"]) for row in rows]
    mix_ask = [parse_float(row["mix_ask"]) for row in rows]
    mix_answer = [parse_float(row["mix_answer"]) for row in rows]
    mix_refuse = [parse_float(row["mix_refuse"]) for row in rows]
    ax.stackplot(iters, mix_ask, mix_answer, mix_refuse, labels=["Ask", "Answer", "Refuse"])
    ax.set_title("Suite Mix Over Time")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Mix")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def build_suite_hardening_plot(rows: list[dict[str, str]], output: Path) -> None:
    fig, ax = plt.subplots()
    iters = [parse_int(row["iter"]) for row in rows]
    constraint_levels = [parse_int(row["constraint_level"]) for row in rows]
    ax.plot(iters, constraint_levels, marker="o", label="Constraint level")

    marker_map = {"low": "o", "med": "s", "high": "^"}
    for strictness, marker in marker_map.items():
        subset_iters = [
            parse_int(row["iter"])
            for row in rows
            if row["format_strictness"].strip().lower() == strictness
        ]
        subset_levels = [
            parse_int(row["constraint_level"])
            for row in rows
            if row["format_strictness"].strip().lower() == strictness
        ]
        if subset_iters:
            ax.scatter(
                subset_iters,
                subset_levels,
                marker=marker,
                label=f"Format strictness: {strictness}",
            )

    ax.set_title("Suite Hardening")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Constraint Level")
    ax.set_ylim(0, max(constraint_levels) + 1)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def build_quality_gates_plot(rows: list[dict[str, str]], output: Path) -> None:
    fig, ax = plt.subplots()
    iters = [parse_int(row["iter"]) for row in rows]
    stabilisation_runs = [parse_int(row["stabilisation_runs"]) for row in rows]
    ax.bar(iters, stabilisation_runs, label="Stabilisation runs")

    marker_height = max(max(stabilisation_runs), 1)
    stabilised_numeric = [
        1 if row["stabilised"].strip().lower() == "yes" else 0 for row in rows
    ]
    ax.scatter(
        iters,
        [value * marker_height for value in stabilised_numeric],
        marker="D",
        label="Stabilised",
    )

    ax.set_title("Quality Gates")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Runs")
    ax.set_ylim(0, marker_height + 1)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def build_dashboard(iter_summary: list[dict[str, str]], suite_progress: list[dict[str, str]]) -> str:
    latest_iter = max(parse_int(row["iter"]) for row in iter_summary)
    latest_summary = next(row for row in iter_summary if parse_int(row["iter"]) == latest_iter)
    suite_latest = next(row for row in suite_progress if parse_int(row["iter"]) == latest_iter)

    mix_text = (
        f"Ask {parse_float(suite_latest['mix_ask']):.0%} / "
        f"Answer {parse_float(suite_latest['mix_answer']):.0%} / "
        f"Refuse {parse_float(suite_latest['mix_refuse']):.0%}"
    )

    snapshot_lines = [
        "**Latest snapshot**",
        "",
        f"- Iteration: {parse_int(latest_summary['iter'])}",
        f"- Date (UTC): {latest_summary['date_utc']}",
        f"- Items: {parse_int(latest_summary['n'])}",
        f"- OK rate: {parse_float(latest_summary['ok_rate']):.3f}",
        f"- Suite version: {suite_latest['suite_version']}",
        f"- Constraint level: {parse_int(suite_latest['constraint_level'])}",
        f"- Mix: {mix_text}",
        f"- Stabilised: {format_yes_no(suite_latest['stabilised'])}",
    ]

    table_headers = [
        "iter",
        "date_utc",
        "suite_version",
        "constraint_level",
        "suite_changes",
        "stabilised",
    ]
    table_rows = []
    for row in suite_progress:
        table_rows.append(
            [
                str(parse_int(row["iter"])),
                str(row["date_utc"]),
                str(row["suite_version"]),
                str(parse_int(row["constraint_level"])),
                str(row["suite_changes"]),
                format_yes_no(row["stabilised"]),
            ]
        )

    table_markdown = render_table(table_headers, table_rows)

    content = "\n".join(
        [
            "# Epistemic Calibration Metrics Dashboard",
            "",
            *snapshot_lines,
            "",
            "## Progress charts",
            "",
            "![ok rate](../assets/plots/ok_rate.png)",
            "",
            "![suite mix](../assets/plots/mix_over_time.png)",
            "",
            "![suite hardening](../assets/plots/suite_hardening.png)",
            "",
            "![quality gates](../assets/plots/quality_gates.png)",
            "",
            "## Suite hardening narrative",
            "",
            table_markdown,
            "",
            "## Data policy",
            "",
            "No raw prompts, outputs, or per-item logs are published.",
            "Only aggregated iteration-level metrics are shown.",
            "",
            "## How to reproduce",
            "",
            "```bash",
            "python scripts/validate_public_inputs.py && \\",
            "  python scripts/build_dashboard.py",
            "```",
            "",
            "## Update cadence",
            "",
            "Dashboard artefacts are regenerated on every push to main and should be updated",
            "whenever new iteration rows are added to the CSVs.",
        ]
    )
    return content + "\n"


def main() -> None:
    iter_summary = sorted(load_csv(DATA_DIR / "iter_summary.csv"), key=lambda r: parse_int(r["iter"]))
    suite_progress = sorted(load_csv(DATA_DIR / "suite_progress.csv"), key=lambda r: parse_int(r["iter"]))

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    build_ok_rate_plot(iter_summary, ASSETS_DIR / "ok_rate.png")
    build_mix_plot(suite_progress, ASSETS_DIR / "mix_over_time.png")
    build_suite_hardening_plot(suite_progress, ASSETS_DIR / "suite_hardening.png")
    build_quality_gates_plot(suite_progress, ASSETS_DIR / "quality_gates.png")

    dashboard_md = build_dashboard(iter_summary, suite_progress)
    (DASHBOARD_DIR / "index.md").write_text(dashboard_md, encoding="utf-8")


if __name__ == "__main__":
    main()
