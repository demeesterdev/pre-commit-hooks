# pre-commit-hooks

Some git hooks for pre-commit.

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/demeesterdev/pre-commit-hooks
  rev: v0.0.1 # Use the ref you want to point at
  hooks:
    - id: no-kubernetes-secrets
  # -   id: ...
```

### Hooks available

#### `detect-kubernetes-secrets`

Detects kubernetes secret manifests in yaml files.

#### `check-kubernetes-secrets-are-sops-encrypted`

checks that kubernetes secret manifests in yaml files are encrypted with sops

#### `check-yaml`

> sourced from https://github.com/pre-commit/pre-commit-hooks

Attempts to load all yaml files to verify syntax.

- `--allow-multiple-documents` - allow yaml files which use the
  [multi-document syntax](http://www.yaml.org/spec/1.2/spec.html#YAML)
- `--unsafe` - Instead of loading the files, simply parse them for syntax.
  A syntax-only check enables extensions and unsafe constructs which would
  otherwise be forbidden. Using this option removes all guarantees of
  portability to other yaml implementations.
  Implies `--allow-multiple-documents`.
