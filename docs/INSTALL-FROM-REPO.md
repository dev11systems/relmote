# Install directly from the Relmote repository

During active development, installing directly from the GitHub repository is a first-class preview path.

## Recommended: pipx

```bash
pipx install 'git+https://github.com/dev11systems/relmote.git'
```

Then:

```bash
relmote
```

Why pipx:

- isolated application environment;
- does not require a system-wide Python package install;
- avoids fighting distro-managed Python environments;
- gives the user a normal `relmote` command;
- easy upgrade/uninstall.

## Upgrade from the repository

```bash
pipx upgrade relmote
```

If pipx does not update a VCS install as expected for a particular version, reinstall explicitly:

```bash
pipx install --force 'git+https://github.com/dev11systems/relmote.git'
```

## Uninstall

```bash
pipx uninstall relmote
```

## Specific branch/tag/commit

Branch:

```bash
pipx install 'git+https://github.com/dev11systems/relmote.git@main'
```

Tag:

```bash
pipx install 'git+https://github.com/dev11systems/relmote.git@preview-0.1'
```

Commit:

```bash
pipx install 'git+https://github.com/dev11systems/relmote.git@<commit-sha>'
```

Pinning a tested commit is useful during preview testing.

## Helper installer

The repository also contains:

```text
scripts/install-from-repo.sh
```

It uses pipx when available and otherwise explains how to install pipx on common Linux distributions.

## Clone-and-run development path

For contributors:

```bash
git clone https://github.com/dev11systems/relmote.git
cd relmote
./scripts/preview-linux.sh
```

This keeps an editable source checkout and is better for development than ordinary use.

## Avoid system-Python hacks

Do not make this the recommended path:

```text
sudo pip install ...
pip --break-system-packages ...
```

Relmote should coexist with the operating system rather than teaching users to bypass distro package protections.

## Future

Repo installation is complementary to:

- standalone release binary;
- AppImage;
- deb/rpm;
- distro/community packages.

The repository path is especially useful while Relmote is moving quickly.
