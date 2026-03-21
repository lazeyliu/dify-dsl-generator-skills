from __future__ import annotations

import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUBY_VALIDATOR = REPO_ROOT / "scripts" / "validate_skill_md.rb"
QUICK_VALIDATE = REPO_ROOT / "scripts" / "quick_validate.py"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class ValidateSkillMdTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = Path(tempfile.mkdtemp(prefix="skill-md-validate-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)

    def test_ruby_validator_rejects_invalid_frontmatter_yaml(self) -> None:
        skill_dir = self.tempdir / "skills" / "demo-skill"
        write_text(
            skill_dir / "SKILL.md",
            """
            ---
            name demo-skill
            description: 缺少冒号后的合法 YAML
            ---

            # demo-skill
            """,
        )

        result = subprocess.run(
            ["ruby", str(RUBY_VALIDATOR), str(self.tempdir)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("frontmatter", result.stdout + result.stderr)

    def test_quick_validate_runs_skill_md_final_validation(self) -> None:
        skill_dir = self.tempdir / "skills" / "demo-skill"
        write_text(
            skill_dir / "SKILL.md",
            """
            ---
            name: demo-skill
            description: 这里带有 <bad> 标记，应该只被 Ruby 终验拦住
            ---

            # demo-skill
            """,
        )

        result = subprocess.run(
            ["python3", str(QUICK_VALIDATE), str(self.tempdir)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("description 不能包含尖括号", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
