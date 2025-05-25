# Publishing Guide for Maintainers

This guide explains how to publish and update the `fastmcp-tutorial` package on PyPI.

## Prerequisites

### 1. Install Publishing Tools

```bash
# Install build and publishing tools
uv add --dev build twine hatch

# Or with pip
pip install build twine hatch
```

### 2. Set Up PyPI Account

1. Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. Generate API tokens:
   - Go to Account Settings → API tokens
   - Create a new token with appropriate scope
   - Save the token securely

### 3. Configure Authentication

#### Option A: Using keyring (Recommended)
```bash
# Install keyring
pip install keyring

# Store credentials
keyring set https://upload.pypi.org/legacy/ __token__
# Enter your PyPI API token when prompted

keyring set https://test.pypi.org/legacy/ __token__
# Enter your TestPyPI API token when prompted
```

#### Option B: Using .pypirc file
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = your-pypi-api-token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-testpypi-api-token
```

## Publishing Workflow

### 1. Pre-publish Checklist

- [ ] Update version number in `pyproject.toml` and `src/fastmcp_tutorial/__init__.py`
- [ ] Update README.md with any new features or changes
- [ ] Ensure all tests pass: `fastmcp-tutorial-test`
- [ ] Update CHANGELOG.md (if you create one)
- [ ] Commit and tag the release

### 2. Version Management

Update version in two places:

**pyproject.toml:**
```toml
[project]
version = "1.1.0"  # Update this
```

**src/fastmcp_tutorial/__init__.py:**
```python
__version__ = "1.1.0"  # Update this
```

### 3. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build

# Or with uv
uv build
```

This creates:
- `dist/fastmcp_tutorial-1.0.0.tar.gz` (source distribution)
- `dist/fastmcp_tutorial-1.0.0-py3-none-any.whl` (wheel distribution)

### 4. Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ fastmcp-tutorial

# Test the installation
fastmcp-tutorial --version
fastmcp-tutorial-test
```

### 5. Publish to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Verify on PyPI
pip install fastmcp-tutorial
fastmcp-tutorial --version
```

### 6. Tag the Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Updating an Existing Package

### 1. Version Bump

For updates, increment the version following [Semantic Versioning](https://semver.org/):

- **Patch** (1.0.0 → 1.0.1): Bug fixes
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Major** (1.0.0 → 2.0.0): Breaking changes

### 2. Update Process

```bash
# 1. Update version numbers (see Version Management above)
# 2. Test locally
fastmcp-tutorial-test

# 3. Build new version
rm -rf dist/
python -m build

# 4. Test on TestPyPI
python -m twine upload --repository testpypi dist/*

# 5. Publish to PyPI
python -m twine upload dist/*

# 6. Tag the release
git tag v1.1.0
git push origin v1.1.0
```

## Automation Options

### GitHub Actions (Recommended)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add your PyPI API token as a GitHub secret named `PYPI_API_TOKEN`.

## Troubleshooting

### Common Issues

1. **Version already exists**: Increment version number
2. **Authentication failed**: Check your API tokens
3. **File already uploaded**: Use `--skip-existing` flag
4. **Package name taken**: Choose a different name in `pyproject.toml`

### Useful Commands

```bash
# Check package metadata
python -m twine check dist/*

# Validate package structure
hatch build --check

# View package contents
tar -tzf dist/fastmcp-tutorial-1.0.0.tar.gz
unzip -l dist/fastmcp_tutorial-1.0.0-py3-none-any.whl
```

## Security Best Practices

1. **Use API tokens** instead of passwords
2. **Store tokens securely** (keyring or environment variables)
3. **Test on TestPyPI first** before publishing to PyPI
4. **Enable 2FA** on your PyPI account
5. **Regularly rotate API tokens**
6. **Use minimal scope tokens** (project-specific when possible)

## Resources

- [PyPI Documentation](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)