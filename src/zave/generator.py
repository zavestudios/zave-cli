"""Workload artifact generator."""

from pathlib import Path
from typing import Optional
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape


class WorkloadGenerator:
    """Generates platform-compliant workload artifacts from contract parameters."""

    def __init__(
        self,
        name: str,
        runtime: str,
        exposure: str,
        delivery: str,
        output_dir: Path,
    ):
        self.name = name
        self.runtime = runtime
        self.exposure = exposure
        self.delivery = delivery
        self.output_dir = Path(output_dir)

        # Create jinja2 environment for templates
        self.env = Environment(
            loader=PackageLoader("zave", "templates"),
            autoescape=select_autoescape(),
            keep_trailing_newline=True,
        )

    def _ensure_dir(self, path: Path):
        """Ensure directory exists."""
        path.mkdir(parents=True, exist_ok=True)

    def _write_file(self, relative_path: str, content: str):
        """Write content to file relative to output_dir."""
        file_path = self.output_dir / relative_path
        self._ensure_dir(file_path.parent)
        file_path.write_text(content)

    def generate_contract(self):
        """Generate zave.yaml contract."""
        contract = {
            "apiVersion": "zave.io/v1",
            "kind": "Workload",
            "metadata": {"name": self.name},
            "spec": {
                "runtime": self.runtime,
                "exposure": self.exposure,
                "delivery": self.delivery,
            },
        }
        content = yaml.dump(contract, default_flow_style=False, sort_keys=False)
        self._write_file("zave.yaml", content)

    def generate_dockerfile(self):
        """Generate runtime-specific Dockerfile."""
        template = self.env.get_template(f"Dockerfile.{self.runtime}.j2")
        content = template.render(name=self.name)
        self._write_file("Dockerfile", content)

    def generate_docker_compose(self):
        """Generate docker-compose.yml for local development."""
        template = self.env.get_template("docker-compose.yml.j2")
        content = template.render(
            name=self.name,
            runtime=self.runtime,
        )
        self._write_file("docker-compose.yml", content)

    def generate_readme(self):
        """Generate README.md with Local Development section."""
        template = self.env.get_template("README.md.j2")
        content = template.render(
            name=self.name,
            runtime=self.runtime,
        )
        self._write_file("README.md", content)

    def generate_env_example(self):
        """Generate .env.example for local development."""
        template = self.env.get_template(".env.example.j2")
        content = template.render(
            name=self.name,
            runtime=self.runtime,
        )
        self._write_file(".env.example", content)

    def generate_workflows(self):
        """Generate GitHub Actions workflows."""
        template = self.env.get_template("workflows/build.yaml.j2")
        content = template.render(name=self.name)
        self._write_file(".github/workflows/build.yaml", content)

    def generate_project_structure(self):
        """Generate runtime-specific project structure."""
        if self.runtime == "python":
            self._generate_python_structure()
        elif self.runtime == "nodejs":
            self._generate_nodejs_structure()
        elif self.runtime == "go":
            self._generate_go_structure()
        # container runtime doesn't need additional structure

    def _generate_python_structure(self):
        """Generate Python project structure."""
        # Create src directory with __init__.py
        self._write_file(f"src/{self.name}/__init__.py", '"""Main application module."""\n')

        # Create main.py
        template = self.env.get_template("python/main.py.j2")
        content = template.render(name=self.name)
        self._write_file(f"src/{self.name}/main.py", content)

        # Create requirements.txt
        template = self.env.get_template("python/requirements.txt.j2")
        content = template.render()
        self._write_file("requirements.txt", content)

        # Create requirements-dev.txt
        template = self.env.get_template("python/requirements-dev.txt.j2")
        content = template.render()
        self._write_file("requirements-dev.txt", content)

        # Create tests directory
        self._write_file("tests/__init__.py", "")
        template = self.env.get_template("python/test_main.py.j2")
        content = template.render(name=self.name)
        self._write_file("tests/test_main.py", content)

    def _generate_nodejs_structure(self):
        """Generate Node.js project structure."""
        # Create package.json
        template = self.env.get_template("nodejs/package.json.j2")
        content = template.render(name=self.name)
        self._write_file("package.json", content)

        # Create src/index.js
        template = self.env.get_template("nodejs/index.js.j2")
        content = template.render(name=self.name)
        self._write_file("src/index.js", content)

    def _generate_go_structure(self):
        """Generate Go project structure."""
        # Create go.mod
        template = self.env.get_template("go/go.mod.j2")
        content = template.render(name=self.name)
        self._write_file("go.mod", content)

        # Create main.go
        template = self.env.get_template("go/main.go.j2")
        content = template.render(name=self.name)
        self._write_file("cmd/main.go", content)

    def generate_gitignore(self):
        """Generate .gitignore for the runtime."""
        template = self.env.get_template(f"gitignore.{self.runtime}.j2")
        content = template.render()
        self._write_file(".gitignore", content)
