"""Initialize a new workload repository."""

import os
from pathlib import Path
import click
import yaml
from zave.generator import WorkloadGenerator


@click.command()
@click.argument("name")
@click.option(
    "--runtime",
    type=click.Choice(["python", "nodejs", "go", "container"], case_sensitive=False),
    default="python",
    help="Workload runtime type",
)
@click.option(
    "--exposure",
    type=click.Choice(["public", "internal", "none"], case_sensitive=False),
    default="none",
    help="Workload exposure level",
)
@click.option(
    "--delivery",
    type=click.Choice(["rolling", "blue-green", "canary"], case_sensitive=False),
    default="rolling",
    help="Deployment delivery strategy",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default=".",
    help="Output directory (defaults to current directory)",
)
def init(name, runtime, exposure, delivery, output_dir):
    """Initialize a new platform workload.

    Creates a new workload repository with:
    - zave.yaml contract
    - Dockerfile (runtime-specific)
    - docker-compose.yml for local development
    - .env.example
    - README.md with Local Development section
    - .github/workflows/build.yaml
    - Runtime-specific project structure

    Example:

        zave init my-service --runtime python --exposure internal
    """
    click.echo(f"Initializing workload: {name}")
    click.echo(f"  Runtime: {runtime}")
    click.echo(f"  Exposure: {exposure}")
    click.echo(f"  Delivery: {delivery}")
    click.echo()

    # Determine output path
    output_path = Path(output_dir) / name
    if output_path.exists():
        click.confirm(
            f"Directory {output_path} already exists. Overwrite?",
            abort=True,
        )

    # Create generator
    generator = WorkloadGenerator(
        name=name,
        runtime=runtime,
        exposure=exposure,
        delivery=delivery,
        output_dir=output_path,
    )

    try:
        # Generate all artifacts
        click.echo("Generating contract...")
        generator.generate_contract()

        click.echo("Generating Dockerfile...")
        generator.generate_dockerfile()

        click.echo("Generating docker-compose.yml...")
        generator.generate_docker_compose()

        click.echo("Generating README.md...")
        generator.generate_readme()

        click.echo("Generating .env.example...")
        generator.generate_env_example()

        click.echo("Generating GitHub workflows...")
        generator.generate_workflows()

        click.echo("Generating project structure...")
        generator.generate_project_structure()

        click.echo("Generating .gitignore...")
        generator.generate_gitignore()

        click.echo()
        click.echo(f"Workload '{name}' initialized successfully.")
        click.echo()
        click.echo("Next steps:")
        click.echo(f"  1. cd {name}")
        click.echo("  2. Review and customize zave.yaml")
        click.echo("  3. Implement your application code")
        click.echo("  4. Test locally: docker-compose up")
        click.echo("  5. Commit and push to trigger CI/CD")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
