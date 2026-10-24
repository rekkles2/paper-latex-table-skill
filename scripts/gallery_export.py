"""Helpers for exporting a public gallery without private references."""


def _has_private_reference_path(value):
    import html
    import re
    from urllib.parse import unquote

    text = html.unescape(unquote(str(value))).replace("\\", "/")
    return re.search(
        r"(?i)(?:^|/)(?:examples/references|assets/cases/local)(?=$|/|[?#\s\"'<>),;])",
        text,
    ) is not None


def _scrub_catalog(value, drop):
    if isinstance(value, dict):
        if value.get("private_reference") is True:
            return drop
        result = {}
        for key, item in value.items():
            if _has_private_reference_path(key):
                continue
            cleaned = _scrub_catalog(item, drop)
            if cleaned is not drop:
                result[key] = cleaned
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            cleaned = _scrub_catalog(item, drop)
            if cleaned is not drop:
                result.append(cleaned)
        return result
    if isinstance(value, str) and _has_private_reference_path(value):
        return drop
    return value


def _sanitize_existing_catalog(entries):
    import json

    key = "paper-latex-table-skill/docs/example-catalog.json"
    if key not in entries:
        return
    value = entries[key]
    try:
        if isinstance(value, bytes):
            catalog = json.loads(value.decode("utf-8"))
        elif isinstance(value, str):
            catalog = json.loads(value)
        else:
            catalog = value
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid existing example catalog") from exc

    drop = object()
    cleaned = _scrub_catalog(catalog, drop)
    if cleaned is drop:
        cleaned = {}
    entries[key] = (json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def enhance_entries(entries, root):
    """Add public example assets and scrub private paths from archive entries."""
    import json
    import os
    from pathlib import Path, PurePosixPath

    def has_private_path(value):
        parts = [part for part in str(value).replace("\\", "/").split("/") if part]
        return any(
            parts[index:index + 2] == ["examples", "references"]
            or parts[index:index + 3] == ["assets", "cases", "local"]
            for index in range(len(parts) - 1)
        )

    for name in list(entries):
        if has_private_path(name):
            del entries[name]

    _sanitize_existing_catalog(entries)

    repository_root = Path(root).resolve(strict=True)
    public_root = repository_root / "examples" / "public"
    if not public_root.is_dir():
        return entries

    public_real = public_root.resolve(strict=True)
    try:
        public_real.relative_to(repository_root)
    except ValueError as exc:
        raise ValueError("Public example root escapes repository: {}".format(public_root)) from exc

    allowed_suffixes = {".tex", ".png", ".pdf", ".jpg", ".json"}
    pending = [(public_root, PurePosixPath())]
    visited_directories = set()

    while pending:
        directory, relative_directory = pending.pop()
        real_directory = directory.resolve(strict=True)
        try:
            real_directory.relative_to(public_real)
        except ValueError as exc:
            raise ValueError(
                "Public example path escapes examples/public: {}".format(directory)
            ) from exc

        if real_directory in visited_directories:
            continue
        visited_directories.add(real_directory)

        try:
            children = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise ValueError(
                "Cannot inspect public example directory: {}".format(directory)
            ) from exc

        for child in children:
            if child.name.startswith(".") or child.name == "__pycache__":
                continue
            path = Path(child.path)
            try:
                resolved = path.resolve(strict=True)
                resolved.relative_to(public_real)
            except (OSError, ValueError) as exc:
                raise ValueError(
                    "Public example path escapes examples/public: {}".format(path)
                ) from exc

            relative_path = relative_directory / child.name
            if child.is_dir(follow_symlinks=True):
                pending.append((path, relative_path))
                continue
            if not child.is_file(follow_symlinks=True):
                continue
            if path.suffix.lower() not in allowed_suffixes:
                continue

            archive_path = PurePosixPath("examples") / "public" / relative_path
            if has_private_path(archive_path.as_posix()):
                continue

            data = resolved.read_bytes()
            if path.name == "example-catalog.json":
                try:
                    catalog = json.loads(data.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ValueError("Invalid public example catalog: {}".format(path)) from exc
                drop = object()
                catalog = _scrub_catalog(catalog, drop)
                if catalog is drop:
                    catalog = {}
                data = (json.dumps(catalog, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            elif path.suffix.lower() in {".tex", ".json"}:
                if _has_private_reference_path(data.decode("utf-8", errors="replace")):
                    raise ValueError(
                        "Public example contains a private-reference path: {}".format(path)
                    )

            entries["paper-latex-table-skill/" + archive_path.as_posix()] = data

    return entries


def check_private_links(markdown):
    """Reject private-reference links and return the Markdown unchanged."""
    import html
    import re
    from urllib.parse import unquote

    candidates = []
    markdown_link = re.compile(
        r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))",
        re.MULTILINE,
    )
    for match in markdown_link.finditer(markdown):
        candidates.append(match.group(1) or match.group(2))

    reference_definition = re.compile(
        r"^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))",
        re.MULTILINE,
    )
    for match in reference_definition.finditer(markdown):
        candidates.append(match.group(1) or match.group(2))

    html_attribute = re.compile(
        r"\b(?:src|href)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
        re.IGNORECASE,
    )
    for match in html_attribute.finditer(markdown):
        candidates.append(match.group(1) or match.group(2) or match.group(3))

    for candidate in candidates:
        if _has_private_reference_path(html.unescape(unquote(candidate))):
            raise ValueError(
                "Public Markdown links to a private reference: {}".format(candidate)
            )
    return markdown
