#!/usr/bin/env python3
"""Fetch a technology icon and print it ready to inline in a diagram.

Icons come from marwin1991/profile-technology-icons (286 colour PNG logos).
That repository ships no licence, so the PNGs are never committed here: this
script downloads one at generation time, downsizes it, caches it under
~/.cache/diagram-design-mono/techicons, and prints an SVG <image> whose href is
a base64 data:image/png URL. The diagram stays a single self-contained file,
and self_check.py accepts data:image URLs.

    python3 scripts/techicon.py list [query]
    python3 scripts/techicon.py find "Spring Boot"
    python3 scripts/techicon.py snippet kafka --x 120 --y 86 [--size 24]
    python3 scripts/techicon.py datauri postgresql

Stdlib only. Downsizing uses Pillow when installed, else macOS `sips`, else
keeps the original file and warns about its size.
"""

from __future__ import annotations

import argparse
import base64
import difflib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

RAW_URL = "https://raw.githubusercontent.com/marwin1991/profile-technology-icons/main/icons/{name}.png"
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "diagram-design-mono" / "techicons"
PIXELS = 64  # stored size: sharp up to 32px display on a 2x screen, a few KB each
LARGE = 24_000  # warn above this many bytes of PNG per icon

# Snapshot of icons/*.png on main (286 names). Unknown names are still tried
# against the repository, so new upstream icons work without editing this list.
NAMES = """
    _net_core activemq amd_vivado android android_studio angular ansible ant_design apache_camel
    apache_netbeans apache_solr apache_spark appcode appwrite arcgis arch_linux arduino
    asahi_linux astro atom auth0 aws babel backbone_js bash bitbucket blazor bootstrap
    browsersync bulma bun_js c# c++ c cachyos canva cargo cassandra chai chainlink chakra_ui
    ci_cd cloudflare cockroachdb codeberg consul coral_ai couchdb css cucumber cypress dart
    databricks digital_ocean directus django docker eclipse elasticsearch electron elementary_os
    elixir ember_js emqx erlang ethereum expo express fastapi fastify fedora figma firebase fish
    flask flutter flyway fme fortran foundry freeBSD gatsby gcp gdal geopandas geoserver git
    github githubactions gitlab go godot google_earth_engine graalvm grafana graphene_os graphql
    groovy grpc grunt gulp hadoop hardhat hazelcast hibernate hive html http huggingface
    ibm_cloud intellij ios java javascript jboss jenkins jest jetty jira jujutsu junit
    jupyter_notebook kafka kali_linux kotlin kubernetes langchain_icon laravel latex leaflet
    linux linux_mint liquibase loki lombok lua lucide macos mapstruct mariadb marionette
    material_design material_ui materialize matlab maven mendeley metamask micrometer micronaut
    microsoft_azure mocha mocikto monero mongodb mosquitto mqtt mqtt_js mssql mysql neo4j neovim
    nest_js netbird next_js next_ui nextcloud nginx nixos node_js nodegui npm numpy nushell
    nuxt_js odoo openresty opentelemetry oracle pandas php php_(elephpant) phpstorm pihole pinia
    play_framework playwright podman postgresql postman prisma prometheus proxmox pug puppet
    puppeteer pycharm pydantic pygame pytest python pytorch qgis qt quarkus rabbitmq
    raspberri_pi react react_query realm redis redux rest robot_framework rpg_maker ruby
    ruby_on_rails rubygems rust sass sbt scala selenium shadcn_ui soap solana solidity sonarqube
    spock spring spring_boot spyder sqlalchemy sqlite ssh stmicroelectronics strapi streamlit
    struts styled-components sublime_text supabase svelte swagger swift tailwind_css tempo
    tensorflow terraform testcontainers thanos tomcat trpc turborepo typescript typst ubuntu
    uniswap unity unreal_engine vaadin vault vercel vim visual_studio_code vite vscodium vue_js
    vuetify_js webassembly webpack websocket webstorm wildfly windows wix wordpress wsl
    wxwidgets xcode yarn zed_ide zero_the_ziguana ziglang zotero zsvirt
""".split()

ALIASES = {
    "k8s": "kubernetes", "postgres": "postgresql", "psql": "postgresql", "node": "node_js",
    "nodejs": "node_js", "js": "javascript", "ts": "typescript", "golang": "go", "spark": "apache_spark",
    "solr": "apache_solr", "camel": "apache_camel", "azure": "microsoft_azure", "google_cloud": "gcp",
    "springboot": "spring_boot", "csharp": "c#", "cpp": "c++", "dotnet": "_net_core", "_net": "_net_core",
    "vscode": "visual_studio_code", "tailwind": "tailwind_css", "nextjs": "next_js", "vue": "vue_js",
    "nestjs": "nest_js", "rabbit": "rabbitmq", "es": "elasticsearch", "sql_server": "mssql",
    "github_actions": "githubactions", "otel": "opentelemetry",
}


def normalize(text: str) -> str:
    key = re.sub(r"[\s.\-/]+", "_", text.strip().lower())
    key = key if key == "_net" else key.strip("_")
    return ALIASES.get(key, ALIASES.get(key.replace("_", ""), key))


def resolve(text: str) -> tuple[str, list[str]]:
    key = normalize(text)
    if key in NAMES:
        return key, []
    compact = key.replace("_", "")
    for name in NAMES:
        if name.replace("_", "") == compact:
            return name, []
    return key, difflib.get_close_matches(key, NAMES, n=5, cutoff=0.5)


def download(name: str) -> bytes:
    url = RAW_URL.format(name=urllib.parse.quote(name))
    with urllib.request.urlopen(url, timeout=20) as response:
        data = response.read()
    if not data.startswith(b"\x89PNG"):
        raise ValueError(f"{url} did not return a PNG")
    return data


def downsize(data: bytes) -> bytes:
    try:
        from io import BytesIO
        from PIL import Image  # type: ignore

        image = Image.open(BytesIO(data)).convert("RGBA")
        image.thumbnail((PIXELS, PIXELS), Image.LANCZOS)
        out = BytesIO()
        image.save(out, format="PNG", optimize=True)
        return out.getvalue()
    except ImportError:
        pass
    if shutil.which("sips"):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "icon.png"
            path.write_bytes(data)
            subprocess.run(["sips", "-Z", str(PIXELS), str(path)], check=True, capture_output=True)
            return path.read_bytes()
    print(f"warning: no Pillow or sips; keeping the original {len(data)}-byte PNG", file=sys.stderr)
    return data


def icon_png(name: str) -> bytes:
    cached = CACHE / f"{name}-{PIXELS}.png"
    if cached.exists():
        return cached.read_bytes()
    data = downsize(download(name))
    CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    if len(data) > LARGE:
        print(f"warning: {name} is {len(data)} bytes after downsizing", file=sys.stderr)
    return data


def data_uri(name: str) -> str:
    return "data:image/png;base64," + base64.b64encode(icon_png(name)).decode("ascii")


def fetch_or_exit(text: str) -> tuple[str, str]:
    name, suggestions = resolve(text)
    try:
        return name, data_uri(name)
    except Exception as exc:  # network error or 404
        hint = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
        print(f"no icon for {text!r} ({exc}).{hint} Fall back to primitive-icons.md or a word tag.", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="print known icon names, optionally filtered")
    listing.add_argument("query", nargs="?", default="")
    find = sub.add_parser("find", help="resolve a technology name to an icon name")
    find.add_argument("name")
    snippet = sub.add_parser("snippet", help="print an SVG <image> element")
    snippet.add_argument("name")
    snippet.add_argument("--x", type=float, required=True)
    snippet.add_argument("--y", type=float, required=True)
    snippet.add_argument("--size", type=int, default=24)
    uri = sub.add_parser("datauri", help="print only the data:image/png URL")
    uri.add_argument("name")
    args = parser.parse_args()

    if args.command == "list":
        query = normalize(args.query) if args.query else ""
        print("\n".join(n for n in NAMES if query in n))
    elif args.command == "find":
        name, suggestions = resolve(args.name)
        if name in NAMES:
            print(name)
        else:
            print(f"not in the snapshot; closest: {', '.join(suggestions) or 'none'}", file=sys.stderr)
            return 1
    elif args.command == "snippet":
        name, href = fetch_or_exit(args.name)
        print(
            f'<image class="techicon" data-techicon="{name}" x="{args.x:g}" y="{args.y:g}" '
            f'width="{args.size}" height="{args.size}" preserveAspectRatio="xMidYMid meet" href="{href}"/>'
        )
    else:
        print(fetch_or_exit(args.name)[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
