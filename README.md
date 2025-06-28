# Restaurant-Website
noh


def load_system_prompt():
    try:
        project_root = Path(__file__).resolve().parent
        prompt_path = project_root / "system_prompt.md"
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"system_prompt.md not found at: {prompt_path}")
        return None