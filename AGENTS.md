# Building a package for this repository

Operate inside a checkout of this repository. Inputs:

- **Paper** — URL, DOI, or an attached PDF
- **Upstream code** — public repository URL
- **Focus** — the methods, tutorial steps, or figures to expose as tools

Goal: one directory under `packages/<package_id>/` that passes this repository's static
validation and is ready to open as a pull request.

## Read first

`schema/package-v1.schema.json`, `docs/contract.md`, `CONTRIBUTING.md`, and `examples/sequence-stats/`
as the reference layout.

## Produce

```
packages/<package_id>/
  metadata.json          strict schema; no fields outside it
  USAGE.md               purpose, inputs, outputs, limits, install steps
  VALIDATION.md          how each tool was verified, and what was not
  LICENSE                license of this submission (never a placeholder)
  NOTICE                 optional; upstream notices when the license requires them
  src/requirements.txt   exactly pinned dependencies (package==version)
  src/<name>_mcp.py      the single MCP entry point
  src/...                further modules
```

## Rules

1. `repo_url` is the canonical `https://github.com/owner/repo` of the **upstream** code — no
   `.git` suffix, no clone URL — paired with its full 40-character commit. Never the wrapper
   repository, never a short hash.
2. `package_id` is lowercase kebab-case, matches the directory name, and stays stable.
3. `doi` and `paper_title` come from the paper; never invent or guess identifiers, and strip any
   trailing punctuation you copied from prose. `doi` may be null when the paper has none;
   `paper_title` is required either way.
4. Exactly one `src/*_mcp.py` entry point. Outside `src/`, only `metadata.json`, `USAGE.md`,
   `LICENSE`, `NOTICE` and `src/requirements.txt` are accepted.
5. Pin every dependency to an exact version; no URLs, no unpinned ranges. The protocol library the
   server speaks is a dependency too, and the runtime environment is rebuilt from
   `src/requirements.txt` alone: whichever FastMCP distribution the entry point imports — the SDK's
   `mcp.server.fastmcp` or the standalone `fastmcp` — must appear there with a version.
6. `src/` may contain Python only. Small read-only tables belong in a Python module as a literal,
   not as a separate data file; anything larger needs maintainer agreement first.
7. Keep the package self-contained: no absolute local paths, no `file://` URIs, no loopback or
   wildcard-bind hosts (`localhost`, `127.0.0.1`, `0.0.0.0`, `::1`), no private or link-local
   addresses, no credentials or tokens, no environment files, logs, notebooks, or real user data.
   Public names such as `localhost.example.com` and `example.com` are fine.
8. Declare a real license in `LICENSE`. A placeholder such as "to be determined" is rejected for a
   published package, and the declared license must allow redistribution of the whole package.
9. State in `USAGE.md` what is and is not reproduced, required inputs, network access, and
   expected resource use.
10. Every published package carries `VALIDATION.md` with the sections
    `## How this was verified` and `## What remains unverified`, and it must name every entry of
    `metadata.json`'s `tools`. Demos are exempt. A verification record is not a formality: it is
    what a reviewer reads instead of taking the submission's word.
11. Do not modify or relax the schema, validator, tests, or workflows to make a package pass.

## Known traps

Each of these passes static validation but stops the package from running. All four surfaced while
building a real package end to end.

1. **A missing FastMCP pin.** The entry point imports a FastMCP distribution, and the environment
   is rebuilt from `src/requirements.txt` only. Leave it out and the server dies with
   `ModuleNotFoundError: No module named 'mcp'` (or `'fastmcp'`) on the user's machine, after review
   has passed.
2. **`from __future__ import annotations`.** With the `mcp` SDK's FastMCP, tool registration
   resolves annotations while importing the module and raises
   `TypeError: issubclass() arg 1 must be a class`. The server exits before answering anything and
   the client only reports a closed connection. Leave the import out.
3. **A leftover `__pycache__`.** Importing the module once leaves `src/__pycache__` inside the
   package, which validation rejects as a generated path. Run local checks with
   `PYTHONDONTWRITEBYTECODE=1`, or delete the directory before validating.
4. **An interpreter that cannot install the pins.** Some dependencies set a floor — scanpy 1.12.4
   requires Python 3.12 or newer. The `python` field in `metadata.json` must name an interpreter
   that can install the pinned requirements and run the server.
5. **A pin that no mirror carries.** The runtime picks a package index by probing mirrors, and they
   lag by different amounts: measured on one day, `anndata==0.13.4` resolved on the Tsinghua mirror
   but not on Aliyun, `0.13.3` resolved on neither, and `0.13.2` resolved on all three including
   upstream PyPI. Pinning the newest patch therefore produces a package that installs on the
   author's machine and fails on a user's, with the failure landing after review. Prefer a release
   that has been out for a while, and check the pins against the indexes the product may use:

   ```sh
   for index in https://mirrors.aliyun.com/pypi/simple \
                https://pypi.tuna.tsinghua.edu.cn/simple https://pypi.org/simple; do
     uv pip install --dry-run --python /tmp/probe/bin/python "anndata==0.13.2" --index-url "$index"
   done
   ```

## The validation record

`VALIDATION.md` states, in the submitter's own words, what was actually exercised and what was
not. Keep it specific — a reviewer checks it against the package:

```markdown
# Validation

## How this was verified

- Environment: Python 3.12; `src/requirements.txt` pins 7 distributions.
- `qc_metrics` — ran against a 30 x 25 synthetic `.h5ad`; checked 30 cells, 25 genes,
  3 mitochondrial genes, and that a missing file is rejected.
- `filter_cells` — same input; checked 30 cells in, 28 out, and that the output file is written.

## What remains unverified

- Agreement with numbers reported in the paper.
- Behaviour on datasets larger than the synthetic input.
```

A delivery from the OmicOS build pipeline can generate this file rather than hand-writing it: see
`tools/from_paper2mcp.py`.

## Verify before reporting

- `python tools/catalog.py validate`
- `python -m unittest discover -s tests -v`
- Start the server once and exercise every tool on small input, including one call it should reject.
  CI never executes package code, so import and registration errors surface only here.
- The package's own checks, recorded exactly as run.
- Re-read every produced file for leaked paths, identifiers, or credentials.

## Report

File tree; commands run and their results; which claims are verified and which are not; what a human
must still confirm (license, redistribution rights, numerical validity).

## Stop

Do not commit, push, or open the pull request. Do not add an entry to `reviews.json`; approvals are
recorded by maintainers only.
