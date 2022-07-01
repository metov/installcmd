from pathlib import Path

BASE_SPEC_PATH = Path(__file__).parent / "commands.yaml"
OVERRIDES_PATH = Path("~/.config/installcmd/overrides.yml").expanduser()
