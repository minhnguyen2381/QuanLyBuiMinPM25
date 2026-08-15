"""Utilities for loading YAML configuration files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "configs"


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML file relative to the project root when needed."""
    cfg_path = Path(path)
    if not cfg_path.is_absolute():
        cfg_path = ROOT_DIR / cfg_path
    with cfg_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_project_configs() -> dict[str, dict[str, Any]]:
    """Load all first-class experiment configuration files."""
    return {
        "data": load_yaml_config(CONFIG_DIR / "data.yaml"),
        "arima": load_yaml_config(CONFIG_DIR / "arima.yaml"),
        "random_forest": load_yaml_config(CONFIG_DIR / "random_forest.yaml"),
        "experiment": load_yaml_config(CONFIG_DIR / "experiment.yaml"),
    }


def project_path(value: str | Path) -> Path:
    """Resolve a config path against the project root."""
    path = Path(value)
    return path if path.is_absolute() else ROOT_DIR / path
