# zave-cli

Platform workload generator - scaffolds contract-compliant repositories with standardized structure.

## Purpose

The `zave` CLI generates new workload repositories from contracts, ensuring consistency across all tenant and portfolio workloads. It implements the generator model defined in `platform-docs/_platform/GENERATOR_MODEL.md`.

This tool unblocks the Formation phase exit criterion: "Generator exists and can create workload repositories end-to-end."

## Installation

```bash
cd /path/to/zave-cli
pip install -e .
```

Verify installation:

```bash
zave --version
```

## Usage

### Initialize New Workload

```bash
zave init <workload-name> [OPTIONS]
```

**Options:**

- `--runtime` - Runtime type: `python`, `nodejs`, `go`, `container` (default: `python`)
- `--exposure` - Exposure level: `public`, `internal`, `none` (default: `none`)
- `--delivery` - Deployment strategy: `rolling`, `blue-green`, `canary` (default: `rolling`)
- `--output-dir` - Output directory (default: current directory)

**Example:**

```bash
zave init my-service --runtime python --exposure internal --delivery rolling
```

### Generated Artifacts

The generator creates a complete workload repository with:

- `zave.yaml` - Platform contract defining workload metadata and requirements
- `Dockerfile` - Runtime-specific container build configuration
- `docker-compose.yml` - Local development environment with hot-reload
- `.env.example` - Environment variable template
- `README.md` - Documentation with "Local Development" section
- `.github/workflows/build.yaml` - CI/CD integration calling shared platform workflows
- `.gitignore` - Runtime-appropriate ignore patterns
- Runtime-specific project structure:
  - Python: `src/<name>/`, `tests/`, `requirements.txt`
  - Node.js: `src/`, `package.json` (planned)
  - Go: `cmd/`, `go.mod` (planned)

## Design Principles

From `GENERATOR_MODEL.md`:

- **Deterministic**: Same contract produces same output
- **Stateless**: No hidden context or external dependencies
- **Observable**: All artifacts are inspectable in Git
- **Replaceable**: Regeneration overwrites safely
- **Complete**: Output is immediately runnable locally

## Current Status

**Implemented:**
- Python runtime support
- Full artifact generation (contract, Dockerfile, compose, workflows, tests)
- CLI with validation and error handling

**Planned:**
- Node.js runtime support (for openclaw)
- Go runtime support
- GitOps manifest generation (Stage 3 generator)
- Capability attachment (Stage 4 generator)

## Development

### Project Structure

```
zave-cli/
├── src/
│   └── zave/
│       ├── cli.py              # CLI entry point
│       ├── commands/
│       │   └── init.py         # Init command implementation
│       ├── generator.py        # Core generator logic
│       └── templates/          # Jinja2 templates
│           ├── Dockerfile.*.j2
│           ├── docker-compose.yml.j2
│           ├── README.md.j2
│           ├── workflows/
│           └── python/
├── pyproject.toml
└── README.md
```

### Adding New Runtime Support

1. Create Dockerfile template: `src/zave/templates/Dockerfile.<runtime>.j2`
2. Create gitignore template: `src/zave/templates/gitignore.<runtime>.j2`
3. Add runtime-specific structure generator in `generator.py`
4. Add runtime templates in `src/zave/templates/<runtime>/`
5. Update CLI choices in `commands/init.py`

### Testing

Generate a test workload and verify output:

```bash
zave init test-app --runtime python
cd test-app
docker-compose up --build
```

## Integration with Platform

The generator is Stage 1 of the platform generator pipeline:

1. **Repository Generator** (this tool) - Creates workload scaffold
2. **Pipeline Generator** (planned) - Derives CI/CD behavior from contract
3. **GitOps Generator** (planned) - Creates deployment manifests
4. **Capability Generator** (planned) - Attaches platform modules

See `platform-docs/_platform/GENERATOR_MODEL.md` for full pipeline design.

## Dogfooding

The `oracle` workload was the first to be regenerated using this tool, validating:

- Python project structure generation
- Docker and docker-compose templates
- Platform workflow integration
- Local development workflow

## Related Documentation

- `platform-docs/_platform/GENERATOR_MODEL.md` - Generator architecture and principles
- `platform-docs/_platform/CONTRACT_SCHEMA.md` - Contract specification
- `platform-docs/_platform/DEVELOPER_EXPERIENCE.md` - Local development standards
- `platform-docs/_platform/REPO_TAXONOMY.md` - Repository classification

## Repository Category

`platform-service` (see `platform-docs/_platform/REPO_TAXONOMY.md`)

Provides reusable capability consumed by platform operations and tenant teams.
