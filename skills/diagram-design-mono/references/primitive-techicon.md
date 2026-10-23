# Technology icons (primitive)

Routed from SKILL.md §6. Colour logos for named technologies, from [marwin1991/profile-technology-icons](https://github.com/marwin1991/profile-technology-icons) (286 PNG icons). Use them so a reader recognises `Kafka` or `PostgreSQL` at a glance instead of decoding a type tag.

## Source and licence

The upstream repository publishes no licence, so this skill never commits its PNGs. `scripts/techicon.py` downloads an icon at generation time, downsizes it to 64px (Pillow, else macOS `sips`), caches it in `~/.cache/diagram-design-mono/techicons/`, and prints it as an SVG `<image>` with a base64 `data:image/png` URL. The diagram stays one self-contained file; `self_check.py` accepts `data:image/*` URLs and still rejects remote ones. The logos remain their owners' trademarks.

Generation needs network access the first time an icon is used. When it is unavailable, fall back as described below.

## Commands

Run from the installed skill directory:

```bash
python3 scripts/techicon.py find "Spring Boot"        # → spring_boot
python3 scripts/techicon.py list kafka                # names containing "kafka"
python3 scripts/techicon.py snippet kafka --x 744 --y 134 --size 24
python3 scripts/techicon.py datauri postgresql        # bare data URL
```

`find` resolves common spellings and aliases (`k8s` → `kubernetes`, `postgres` → `postgresql`, `C#` → `c#`, `.NET` → `_net_core`). An unknown name is still tried upstream, then the script exits non-zero with the closest names.

## When to use one

- **Every node that is a named technology gets its icon.** A node for Kafka, MySQL, Kubernetes, Redis, Spark, Grafana, and so on.
- **Concept nodes do not.** "Job manager", "Checkpoint store", or "User" are roles, not products: use a monochrome glyph from [primitive-icons.md](primitive-icons.md) or a whole-word type tag.
- **No icon in the catalog** (for example Doris or StarRocks): check [primitive-icons.md](primitive-icons.md), which carries some brand silhouettes, then fall back to a whole-word type tag. Never draw or approximate a logo by hand.
- **One icon per node.** An icon replaces the type tag; never show both.
- Icons are identity marks, not signals. They do not count toward the accent budget, never carry meaning through their colour, and never appear in arrow labels.

## Placement

The icon takes the type tag's corner. Paste the `snippet` output inside the node's `<g class="node">`, after the styled `node-box` rect and before the text:

| Node height | Icon size | Position |
|---|---|---|
| 48 to 64 | 24, or 28 for a logo with a wordmark | `x = X + 8`, `y = Y + 6` |
| 72 and up | 28 to 32 | `x = X + 8`, `y = Y + 8` |
| Sequence actor (56) | 24 | `x = X + 8`, `y = Y + 6` |

Many logos carry their name as text (MySQL, PostgreSQL). Under 24px that text turns to noise and the logo reads as a smudge, so never go below 24 for those; a symbol-only logo (Kafka, Hazelcast) can drop to 20 when the node name is long.

```svg
<g class="node">
  <rect x="X" y="Y" width="W" height="H" fill="{paper}"/>
  <rect class="node-box" x="X" y="Y" width="W" height="H" fill="FILL" stroke="STROKE" stroke-width="1"/>
  <image class="techicon" data-techicon="kafka" x="X+8" y="Y+6" width="24" height="24"
         preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,…"/>
  <text …>이벤트 스트림</text>
  <text …>Kafka</text>
</g>
```

- Keep at least 8px between the icon and the node name. If a centred name would reach the icon, widen the box on the 4px grid rather than shrinking the type.
- **Dark skin:** many logos are dark. Put a square in the light `paper` colour (`#f8fafc`, no `rx`) 4px larger than the icon behind it, inset 2px, so the logo stays visible.
- Hover leaves the icon alone: the hover CSS recolours only `.node-box` and text.
- A legend does not list icons. The node's own name says what it is.

## Size budget

A downsized icon is about 4 to 7 KB, or 6 to 9 KB once base64-encoded. Ten icons add under 100 KB to a page. Reuse is free in the cache but each `<image>` carries its own copy, so a diagram that repeats one logo many times (a fleet of identical Kafka brokers) should show it once on the zone or the first node.

## Catalog (286)

Names as `techicon.py` accepts them. Snapshot of `icons/*.png` on `main`; `python3 scripts/techicon.py list` prints the same list.

```text
_net_core activemq amd_vivado android android_studio angular ansible ant_design apache_camel
apache_netbeans apache_solr apache_spark appcode appwrite arcgis arch_linux arduino asahi_linux
astro atom auth0 aws babel backbone_js bash bitbucket blazor bootstrap browsersync bulma bun_js
c# c++ c cachyos canva cargo cassandra chai chainlink chakra_ui ci_cd cloudflare cockroachdb
codeberg consul coral_ai couchdb css cucumber cypress dart databricks digital_ocean directus
django docker eclipse elasticsearch electron elementary_os elixir ember_js emqx erlang ethereum
expo express fastapi fastify fedora figma firebase fish flask flutter flyway fme fortran foundry
freeBSD gatsby gcp gdal geopandas geoserver git github githubactions gitlab go godot
google_earth_engine graalvm grafana graphene_os graphql groovy grpc grunt gulp hadoop hardhat
hazelcast hibernate hive html http huggingface ibm_cloud intellij ios java javascript jboss
jenkins jest jetty jira jujutsu junit jupyter_notebook kafka kali_linux kotlin kubernetes
langchain_icon laravel latex leaflet linux linux_mint liquibase loki lombok lua lucide macos
mapstruct mariadb marionette material_design material_ui materialize matlab maven mendeley
metamask micrometer micronaut microsoft_azure mocha mocikto monero mongodb mosquitto mqtt mqtt_js
mssql mysql neo4j neovim nest_js netbird next_js next_ui nextcloud nginx nixos node_js nodegui
npm numpy nushell nuxt_js odoo openresty opentelemetry oracle pandas php php_(elephpant)
phpstorm pihole pinia play_framework playwright podman postgresql postman prisma prometheus
proxmox pug puppet puppeteer pycharm pydantic pygame pytest python pytorch qgis qt quarkus
rabbitmq raspberri_pi react react_query realm redis redux rest robot_framework rpg_maker ruby
ruby_on_rails rubygems rust sass sbt scala selenium shadcn_ui soap solana solidity sonarqube
spock spring spring_boot spyder sqlalchemy sqlite ssh stmicroelectronics strapi streamlit struts
styled-components sublime_text supabase svelte swagger swift tailwind_css tempo tensorflow
terraform testcontainers thanos tomcat trpc turborepo typescript typst ubuntu uniswap unity
unreal_engine vaadin vault vercel vim visual_studio_code vite vscodium vue_js vuetify_js
webassembly webpack websocket webstorm wildfly windows wix wordpress wsl wxwidgets xcode yarn
zed_ide zero_the_ziguana ziglang zotero zsvirt
```
