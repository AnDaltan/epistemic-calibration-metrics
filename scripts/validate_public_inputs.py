#!/usr/bin/env python3
"""Validate public CSV inputs for the dashboard."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

ITER_SUMMARY_COLUMNS = [
    "iter",
    "date_utc",
    "n",
    "ok_rate",
    "AR",
    "AWI",
    "AWS",
    "notes",
]

SUITE_PROGRESS_COLUMNS = [
    "iter",
    "date_utc",
    "n",
    "mix_ask",
    "mix_answer",
    "mix_refuse",
    "suite_version",
    "suite_changes",
    "constraint_level",
    "generation_required",
    "format_strictness",
    "refusal_slice_enabled",
    "token_constraint_enabled",
    "stabilised",
    "stabilisation_runs",
    "quality_gate_pass",
    "caveats",
]

GLOSSARY_COLUMNS = ["key", "label", "description"]

FORBIDDEN_SUBSTRINGS = [
    "prompt",
    "output",
    "outputs.jsonl",
    "jsonl",
    "fail_reason",
    "regex",
    "pattern",
    "token:",
    "must_include",
    "marker",
    "phishing",
    "doxx",
    "mfa",
    "password extraction",
    "forge",
    "category list",
]

RESTRICTED_NOTE_WORDS = ["phishing", "doxx", "mfa", "password extraction", "forge"]

MAX_CELL_LENGTH = 240
MIX_TOLERANCE = 0.02


class ValidationError(Exception):
    pass


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = [row for row in reader]
        return reader.fieldnames or [], rows
    except Exception as exc:  # pragma: no cover - surfaced in CLI error
        raise ValidationError(f"Failed to read {path.name}: {exc}") from exc


def ensure_expected_columns(columns: list[str], expected: list[str], name: str) -> None:
    if columns != expected:
        raise ValidationError(f"{name} columns must be {expected}, got {columns}")


def ensure_no_forbidden_content(columns: list[str], rows: list[dict[str, str]], name: str) -> None:
    forbidden = [term.lower() for term in FORBIDDEN_SUBSTRINGS]
    for column in columns:
        lower_col = column.lower()
        for term in forbidden:
            if term in lower_col:
                raise ValidationError(f"Forbidden term '{term}' found in column {column} ({name})")
    for row in rows:
        for column in columns:
            value = row.get(column, "")
            text = "" if value is None else str(value)
            if len(text) > MAX_CELL_LENGTH:
                raise ValidationError(
                    f"Cell in {name}.{column} exceeds {MAX_CELL_LENGTH} characters"
                )
            lower_text = text.lower()
            for term in forbidden:
                if term in lower_text:
                    raise ValidationError(
                        f"Forbidden term '{term}' found in {name}.{column}"
                    )


def ensure_restricted_notes(rows: list[dict[str, str]], name: str, columns: list[str]) -> None:
    restricted = [term.lower() for term in RESTRICTED_NOTE_WORDS]
    for row in rows:
        for column in columns:
            value = row.get(column, "")
            if value is None:
                continue
            lower_text = str(value).lower()
            for term in restricted:
                if term in lower_text:
                    raise ValidationError(
                        f"Restricted term '{term}' found in {name}.{column}"
                    )


def parse_float(value: str, name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{name} must be a number") from exc


def parse_int(value: str, name: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{name} must be an integer") from exc


def ensure_range(value: float, name: str, low: float = 0.0, high: float = 1.0) -> None:
    if not (low <= value <= high):
        raise ValidationError(f"{name} must be between {low} and {high}")


def ensure_yes_no(value: str, name: str) -> None:
    if str(value).strip().lower() not in {"yes", "no"}:
        raise ValidationError(f"{name} must be yes/no values")


def validate_iter_summary(path: Path) -> None:
    columns, rows = load_csv(path)
    ensure_expected_columns(columns, ITER_SUMMARY_COLUMNS, path.name)
    ensure_no_forbidden_content(columns, rows, path.name)
    ensure_restricted_notes(rows, path.name, ["notes"])

    for row in rows:
        ensure_range(parse_float(row["ok_rate"], f"{path.name}.ok_rate"), f"{path.name}.ok_rate")
        ensure_range(parse_float(row["AR"], f"{path.name}.AR"), f"{path.name}.AR")
        ensure_range(parse_float(row["AWI"], f"{path.name}.AWI"), f"{path.name}.AWI")
        ensure_range(parse_float(row["AWS"], f"{path.name}.AWS"), f"{path.name}.AWS")

        if parse_int(row["iter"], f"{path.name}.iter") < 0:
            raise ValidationError("iter must be non-negative")
        if parse_int(row["n"], f"{path.name}.n") <= 0:
            raise ValidationError("n must be positive")


def validate_suite_progress(path: Path) -> None:
    columns, rows = load_csv(path)
    ensure_expected_columns(columns, SUITE_PROGRESS_COLUMNS, path.name)
    ensure_no_forbidden_content(columns, rows, path.name)
    ensure_restricted_notes(rows, path.name, ["suite_changes", "caveats"])

    for row in rows:
        mix_ask = parse_float(row["mix_ask"], f"{path.name}.mix_ask")
        mix_answer = parse_float(row["mix_answer"], f"{path.name}.mix_answer")
        mix_refuse = parse_float(row["mix_refuse"], f"{path.name}.mix_refuse")
        for value, name in [
            (mix_ask, f"{path.name}.mix_ask"),
            (mix_answer, f"{path.name}.mix_answer"),
            (mix_refuse, f"{path.name}.mix_refuse"),
        ]:
            ensure_range(value, name)

        mix_sum = mix_ask + mix_answer + mix_refuse
        if abs(mix_sum - 1.0) > MIX_TOLERANCE:
            raise ValidationError("mix columns must sum to approximately 1.0")

        if parse_int(row["constraint_level"], f"{path.name}.constraint_level") < 1:
            raise ValidationError("constraint_level must be >= 1")

        ensure_yes_no(row["generation_required"], f"{path.name}.generation_required")
        ensure_yes_no(row["refusal_slice_enabled"], f"{path.name}.refusal_slice_enabled")
        ensure_yes_no(row["token_constraint_enabled"], f"{path.name}.token_constraint_enabled")
        ensure_yes_no(row["stabilised"], f"{path.name}.stabilised")
        ensure_yes_no(row["quality_gate_pass"], f"{path.name}.quality_gate_pass")

        if str(row["format_strictness"]).strip().lower() not in {"low", "med", "high"}:
            raise ValidationError("format_strictness must be low/med/high")

        if parse_int(row["stabilisation_runs"], f"{path.name}.stabilisation_runs") < 0:
            raise ValidationError("stabilisation_runs must be >= 0")

        if parse_int(row["iter"], f"{path.name}.iter") < 0:
            raise ValidationError("iter must be non-negative")
        if parse_int(row["n"], f"{path.name}.n") <= 0:
            raise ValidationError("n must be positive")


def validate_glossary(path: Path) -> None:
    columns, rows = load_csv(path)
    ensure_expected_columns(columns, GLOSSARY_COLUMNS, path.name)
    ensure_no_forbidden_content(columns, rows, path.name)


def ensure_only_expected_files() -> None:
    allowed = {"iter_summary.csv", "suite_progress.csv", "glossary.csv"}
    for path in DATA_DIR.iterdir():
        if path.is_file() and path.name not in allowed:
            raise ValidationError(f"Unexpected file in data/: {path.name}")
        if path.suffix and path.suffix != ".csv":
            raise ValidationError(f"Unexpected non-CSV file in data/: {path.name}")


def main() -> int:
    try:
        ensure_only_expected_files()
        validate_iter_summary(DATA_DIR / "iter_summary.csv")
        validate_suite_progress(DATA_DIR / "suite_progress.csv")
        glossary_path = DATA_DIR / "glossary.csv"
        if glossary_path.exists():
            validate_glossary(glossary_path)
    except ValidationError as exc:
        print(f"Validation error: {exc}")
        return 1
    print("Public input validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
