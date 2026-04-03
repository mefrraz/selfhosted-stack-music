<div align="center">

<<<<<<< HEAD
# 🎵 selfhosted-stack-music
=======
# 🎵 Self-Hosted Music Stack
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e

**A personal, high-fidelity music infrastructure — fully self-hosted and Docker-ready.**

[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
<<<<<<< HEAD
[![Navidrome](https://img.shields.io/badge/Navidrome-v0.58+-F2711C?logo=musicbrainz&logoColor=white)](https://www.navidrome.org/)
[![Deemix](https://img.shields.io/badge/Deemix-Bambanah-60a5fa?logo=deezer&logoColor=white)](https://github.com/bambanah/deemix)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e.svg)](LICENSE)

[🌐 Website](https://mefrraz.github.io/selfhosted-stack-music) · [📖 Docs](#-quick-start) · [🇵🇹 Português](#-português)
=======
[![Navidrome](https://img.shields.io/badge/Navidrome-Subsonic%20API-F2711C?logo=musicbrainz&logoColor=white)](https://www.navidrome.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

🇬🇧 English | [🇵🇹 Português](#-português)
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e

</div>

---

## 🇬🇧 English

### ✨ Features

| | Feature |
|---|---|
<<<<<<< HEAD
| 🎧 | Stream your entire library via any Subsonic-compatible client (Feishin, Substreamer, Navic…) |
| 📥 | Automated FLAC/MP3 acquisition with complete ID3v2 tagging via Deemix (Bambanah) |
| 🎤 | Mass lyrics sync — LRC embedded directly into audio files, no external `.lrc` files |
| 📻 | Radio station automation via Radio-Browser API, written directly to SQLite |
| 🐳 | Fully containerized — runs anywhere Docker runs |
| 🔒 | HTTPS-ready — works with Nginx Proxy Manager, Traefik, or Caddy |
| 📚 | Multi-library support (Navidrome v0.58+) with per-user access controls |
=======
| 🎧 | Stream your entire music library via any Subsonic-compatible client |
| 📥 | Automated FLAC/MP3 acquisition with full ID3v2 tagging |
| 🎤 | Mass lyrics sync embedded directly into audio files |
| 📻 | Radio station automation via Radio-Browser API |
| 🐳 | Fully containerized — runs anywhere Docker runs |
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e

---

### 🧩 Stack Overview

```
<<<<<<< HEAD
┌──────────────────────────────────────────────────┐
│   Navidrome            :4533                     │  ← Music server & Subsonic API
├──────────────────────────────────────────────────┤
│   Deemix (Bambanah)    :6595                     │  ← Audio acquisition & ID3v2 tagging
├──────────────────────────────────────────────────┤
│   LRCGET               (desktop app)             │  ← Lyrics sync via LRCLIB
├──────────────────────────────────────────────────┤
│   navidrome-radio.py   (CLI script)              │  ← Radio station automation
└──────────────────────────────────────────────────┘
              ↕  Reverse Proxy (HTTPS)
      Nginx Proxy Manager / Traefik / Caddy
=======
┌─────────────────────────────────────────┐
│              Navidrome                  │  ← Music server & streaming API
├─────────────────────────────────────────┤
│     Deemix (Bambanah Edition)           │  ← Audio acquisition & tagging
├─────────────────────────────────────────┤
│              LRCGET                     │  ← Lyrics sync (LRCLIB)
├─────────────────────────────────────────┤
│         navidrome-radio.py              │  ← Radio station automation
└─────────────────────────────────────────┘
         ↕ Reverse Proxy (HTTPS)
   Nginx Proxy Manager / Traefik / Caddy
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e
```

---

### 🚀 Quick Start

#### Prerequisites

<<<<<<< HEAD
- Docker & Docker Compose installed on your host
- A Deezer account (for the ARL token)
- Ports `4533` and `6595` available

#### 1. Get your Deezer ARL token

1. Login to [Deezer](https://www.deezer.com/) on a **desktop browser**
2. Open Developer Tools → `F12` → **Application** → **Cookies** → `deezer.com`
3. Copy the value of the `arl` cookie

> ⚠️ Keep your ARL token private — it grants full access to your Deezer account.

#### 2. docker-compose.yml

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    ports: ["4533:4533"]
    volumes:
      - ./data/navidrome:/data
      - ./music:/music:ro
    environment:
      ND_LOGLEVEL: info
      ND_UI_VAMP_THEME: dark

  deemix:
    image: ghcr.io/bambanah/deemix:latest
    ports: ["6595:6595"]
    volumes:
      - ./music:/downloads
      - ./data/deemix:/config
    environment:
      PUID: 1000
      PGID: 1000
      UMASK_SET: 022
```

#### 3. Start
=======
- Docker & Docker Compose installed
- A [Deezer](https://www.deezer.com/) account (for the ARL token)
- A domain or local network setup for the reverse proxy

#### 1. Get your Deezer ARL token

1. Login to [Deezer](https://www.deezer.com/) on a desktop browser
2. Open Developer Tools → `F12` → **Application** → **Cookies**
3. Copy the value of the `arl` cookie

#### 2. Configure environment variables

```env
PUID=1000
PGID=1000
UMASK_SET=022
ND_LOGLEVEL=info
ND_UI_VAMP_THEME=dark
```

#### 3. Start the stack
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e

```bash
docker compose up -d
```

---

### 🧱 Components

<<<<<<< HEAD
#### 🟣 Navidrome — Core Engine

Open-source music server written in Go, Subsonic-compatible. Think of it as your personal Spotify.

- **Themes:** Dracula, Nord, Dark, Midday, AMusic, SquiddiesGlass and more
- **Notable features (v0.58+):** Multi-library, Scrobble History, Instant Mix via Last.fm/Deezer, plugin system
- **Recommended clients:**
  - 🖥️ Desktop: [Feishin](https://github.com/jeffvli/feishin)
  - 📱 Mobile: [Substreamer](https://substreamerapp.com/) · [Navic](https://github.com/paigely/Navic)

#### 🔵 Deemix (Bambanah Edition) — Audio Acquisition

Actively maintained Docker-optimized fork. Downloads FLAC/MP3 with full ID3v2 metadata. Current version: `3.13.6`.

> ⚠️ Disable the built-in lyrics download — it's unstable. Use **LRCGET** instead.

**Spotify fallback:** Deemix 3.13.x supports resolving Spotify public playlists even when the standard API returns 404.

#### 🟢 LRCGET — Lyrics Management

Official desktop client for [LRCLIB](https://lrclib.net/). Scans your music directory and embeds synchronized LRC lyrics directly into audio file tags.

- Configure: **"Embed lyrics into audio files"** — not external `.lrc` files
- Supports custom/self-hosted LRCLIB instances
- Cross-platform: Windows, macOS, Linux (written in Rust)

#### 🟡 Radio Automation — `navidrome-radio.py`

Uses the [Radio-Browser API](https://www.radio-browser.info/) to populate Navidrome with radio stations via direct SQLite injection — no container restart needed.

- Search by **name** (e.g. `Comercial`, `RFM`), **genre** or **country**
- Pagination support & duplicate detection

```bash
python3 -m venv venv && source venv/bin/activate
pip install requests
=======
#### 🟠 Navidrome — Core Engine

A Subsonic-compliant music server written in Go. Handles library indexing and exposes the API for all clients.

- **Themes:** Dracula, Nord, Dark, Midday, and more
- **Recommended clients:**
  - 🖥️ Desktop: [Feishin](https://github.com/jeffvli/feishin)
  - 📱 Mobile: [Substreamer](https://substreamerapp.com/)

#### 🔵 Deemix (Bambanah Edition) — Audio Acquisition

Primary tool for downloading audio and applying ID3v2 tags.

> ⚠️ **Note:** The built-in lyrics download option is disabled due to API instability. Use **LRCGET** for lyrics post-processing.

#### 🟢 LRCGET — Lyrics Management

Mass-downloads and synchronizes LRC lyrics via [LRCLIB](https://lrclib.net/).

- Configure it to **embed lyrics directly** into audio files (ID3v2 tags) — no external `.lrc` files needed.
- Ensures seamless detection by Navidrome.

#### 🟣 Radio Automation — `navidrome-radio.py`

Interfaces with the [Radio-Browser API](https://www.radio-browser.info/) to populate your Navidrome radio stations.

- Search by **name**, **genre**, or **country**
- Pagination support & duplicate detection
- Writes directly to `navidrome.db` (no container restart needed)

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install requests

# Run
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e
python3 navidrome-radio.py
```

---

### ⚙️ Environment Variables

| Variable | Service | Description | Default |
|---|---|---|---|
| `PUID` | Deemix | Host User ID for file ownership | `1000` |
| `PGID` | Deemix | Host Group ID for file ownership | `1000` |
| `UMASK_SET` | Deemix | File permission mask (`022` = 644/755) | `022` |
| `ND_LOGLEVEL` | Navidrome | Logging verbosity (`info`, `debug`, `error`) | `info` |
| `ND_UI_VAMP_THEME` | Navidrome | Default UI theme | `dark` |

---

### 🌐 Remote Access (Reverse Proxy)

<<<<<<< HEAD
Required for secure WAN exposure (HTTPS):
=======
Required for secure WAN exposure (HTTPS). Choose one:
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e

| Option | Best for |
|---|---|
| [Nginx Proxy Manager](https://nginxproxymanager.com/) | GUI-based, easy SSL via Let's Encrypt |
| [Traefik](https://traefik.io/) | Docker label-based config, power users |
<<<<<<< HEAD
| [Caddy](https://caddyserver.com/) | Minimal config, automatic HTTPS by default |

---
---

## 🇵🇹 Português

### ✨ Funcionalidades

| | Funcionalidade |
|---|---|
| 🎧 | Streaming de toda a biblioteca via qualquer cliente Subsonic (Feishin, Substreamer, Navic…) |
| 📥 | Aquisição automática de FLAC/MP3 com etiquetagem ID3v2 completa via Deemix (Bambanah) |
| 🎤 | Sincronização de letras em massa — LRC embutido nos ficheiros, sem `.lrc` externos |
| 📻 | Automação de rádios via API Radio-Browser, escrito diretamente no SQLite |
| 🐳 | Totalmente containerizado — corre onde Docker correr |
| 🔒 | Pronto para HTTPS — compatível com Nginx Proxy Manager, Traefik ou Caddy |
| 📚 | Suporte multi-biblioteca (Navidrome v0.58+) com controlos de acesso por utilizador |

---

### 🧩 Visão Geral da Stack

```
┌──────────────────────────────────────────────────┐
│   Navidrome            :4533                     │  ← Servidor de música & API Subsonic
├──────────────────────────────────────────────────┤
│   Deemix (Bambanah)    :6595                     │  ← Aquisição de áudio & etiquetagem ID3v2
├──────────────────────────────────────────────────┤
│   LRCGET               (app desktop)             │  ← Sincronização de letras via LRCLIB
├──────────────────────────────────────────────────┤
│   navidrome-radio.py   (script CLI)              │  ← Automação de rádios
└──────────────────────────────────────────────────┘
              ↕  Reverse Proxy (HTTPS)
      Nginx Proxy Manager / Traefik / Caddy
=======
| [Caddy](https://caddyserver.com/) | Minimal setup, automatic HTTPS |

---

---

## 🇵🇹 Português

### ✨ Funcionalidades

| | Funcionalidade |
|---|---|
| 🎧 | Faz streaming da tua biblioteca via qualquer cliente Subsonic |
| 📥 | Aquisição automática de FLAC/MP3 com etiquetagem ID3v2 completa |
| 🎤 | Sincronização de letras em massa, diretamente nos ficheiros de áudio |
| 📻 | Automação de rádios via API Radio-Browser |
| 🐳 | Totalmente containerizado — corre onde Docker correr |

---

### 🧩 Visão Geral da Stack

```
┌─────────────────────────────────────────┐
│              Navidrome                  │  ← Servidor de música & API de streaming
├─────────────────────────────────────────┤
│     Deemix (Versão Bambanah)            │  ← Aquisição de áudio & etiquetagem
├─────────────────────────────────────────┤
│              LRCGET                     │  ← Sincronização de letras (LRCLIB)
├─────────────────────────────────────────┤
│         navidrome-radio.py              │  ← Automação de rádios
└─────────────────────────────────────────┘
         ↕ Reverse Proxy (HTTPS)
   Nginx Proxy Manager / Traefik / Caddy
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e
```

---

### 🚀 Início Rápido

#### Pré-requisitos

- Docker & Docker Compose instalados
<<<<<<< HEAD
- Conta no Deezer (para o token ARL)
- Portas `4533` e `6595` disponíveis

#### 1. Obtém o token ARL do Deezer

1. Faz login no [Deezer](https://www.deezer.com/) num **browser desktop**
2. Abre as Ferramentas de Programador → `F12` → **Application** → **Cookies** → `deezer.com`
3. Copia o valor do cookie `arl`

> ⚠️ Guarda o token ARL em segredo — dá acesso total à tua conta Deezer.

#### 2. docker-compose.yml

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    ports: ["4533:4533"]
    volumes:
      - ./data/navidrome:/data
      - ./music:/music:ro
    environment:
      ND_LOGLEVEL: info
      ND_UI_VAMP_THEME: dark

  deemix:
    image: ghcr.io/bambanah/deemix:latest
    ports: ["6595:6595"]
    volumes:
      - ./music:/downloads
      - ./data/deemix:/config
    environment:
      PUID: 1000
      PGID: 1000
      UMASK_SET: 022
```

#### 3. Iniciar
=======
- Conta no [Deezer](https://www.deezer.com/) (para o token ARL)
- Domínio ou rede local configurada para o reverse proxy

#### 1. Obtém o token ARL do Deezer

1. Faz login no [Deezer](https://www.deezer.com/) num browser desktop
2. Abre as Ferramentas de Programador → `F12` → **Application** → **Cookies**
3. Copia o valor do cookie `arl`

#### 2. Configura as variáveis de ambiente

```env
PUID=1000
PGID=1000
UMASK_SET=022
ND_LOGLEVEL=info
ND_UI_VAMP_THEME=dark
```

#### 3. Inicia a stack
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e

```bash
docker compose up -d
```

---

### 🧱 Componentes

<<<<<<< HEAD
#### 🟣 Navidrome — Motor Central

Servidor de música open-source escrito em Go, compatível com Subsonic. O teu Spotify pessoal.

- **Temas:** Dracula, Nord, Dark, Midday, AMusic, SquiddiesGlass e mais
- **Funcionalidades notáveis (v0.58+):** Multi-biblioteca, Scrobble History, Instant Mix via Last.fm/Deezer, sistema de plugins
- **Clientes recomendados:**
  - 🖥️ Desktop: [Feishin](https://github.com/jeffvli/feishin)
  - 📱 Mobile: [Substreamer](https://substreamerapp.com/) · [Navic](https://github.com/paigely/Navic)

#### 🔵 Deemix (Versão Bambanah) — Aquisição de Áudio

Fork ativamente mantido e otimizado para Docker. Descarrega FLAC/MP3 com metadados ID3v2 completos. Versão atual: `3.13.6`.

> ⚠️ Desativa o download de letras nativo — é instável. Usa o **LRCGET**.

**Fallback Spotify:** O Deemix 3.13.x suporta resolver playlists públicas do Spotify mesmo quando a API devolve 404.

#### 🟢 LRCGET — Gestão de Letras

Cliente oficial do [LRCLIB](https://lrclib.net/). Analisa o diretório de música e embute letras LRC sincronizadas nas tags dos ficheiros de áudio.

- Configura: **"Embutir letras nos ficheiros de áudio"** — não ficheiros `.lrc` externos
- Suporta instâncias LRCLIB personalizadas (self-hosted)
- Multi-plataforma: Windows, macOS, Linux (escrito em Rust)

#### 🟡 Automação de Rádios — `navidrome-radio.py`

Usa a [API Radio-Browser](https://www.radio-browser.info/) para popular o Navidrome com rádios via injeção direta no SQLite — sem reinício do contentor.

- Pesquisa por **nome** (ex: `Comercial`, `RFM`), **género** ou **país**
- Suporte a paginação e deteção de duplicados

```bash
python3 -m venv venv && source venv/bin/activate
=======
#### 🟠 Navidrome — Motor Central

Servidor de música compatível com Subsonic escrito em Go. Gere a indexação da biblioteca e expõe a API para todos os clientes.

- **Temas:** Dracula, Nord, Dark, Midday, e mais
- **Clientes recomendados:**
  - 🖥️ Desktop: [Feishin](https://github.com/jeffvli/feishin)
  - 📱 Mobile: [Substreamer](https://substreamerapp.com/)

#### 🔵 Deemix (Versão Bambanah) — Aquisição de Áudio

Ferramenta principal para descarregar áudio e aplicar tags ID3v2.

> ⚠️ **Nota:** A opção de download de letras nativa deve ser ignorada por instabilidade. Usa o **LRCGET** para embutir letras após o download.

#### 🟢 LRCGET — Gestão de Letras

Descarrega e sincroniza letras LRC em massa via [LRCLIB](https://lrclib.net/).

- Configura para **embutir letras diretamente** nos ficheiros de áudio (tags ID3v2) — sem ficheiros `.lrc` externos.
- Garante deteção automática pelo Navidrome.

#### 🟣 Automação de Rádios — `navidrome-radio.py`

Usa a [API Radio-Browser](https://www.radio-browser.info/) para popular as rádios no Navidrome.

- Pesquisa por **nome** (ex: Comercial, RFM), **género** ou **país**
- Suporte a paginação e deteção de duplicados
- Escreve diretamente no `navidrome.db` (sem reinício do contentor)

```bash
# Configuração
python3 -m venv venv
source venv/bin/activate
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e
pip install requests

# Executar
python3 navidrome-radio.py
```

---

### ⚙️ Variáveis de Ambiente

| Variável | Serviço | Descrição | Valor Sugerido |
|---|---|---|---|
| `PUID` | Deemix | ID do utilizador no host para posse de ficheiros | `1000` |
| `PGID` | Deemix | ID do grupo no host para posse de ficheiros | `1000` |
| `UMASK_SET` | Deemix | Máscara de permissões (`022` = 644/755) | `022` |
| `ND_LOGLEVEL` | Navidrome | Nível de detalhe dos logs (`info`, `debug`) | `info` |
| `ND_UI_VAMP_THEME` | Navidrome | Tema padrão da interface web | `dark` |

---

### 🌐 Acesso Remoto (Reverse Proxy)

<<<<<<< HEAD
Obrigatório para exposição segura à Internet (HTTPS):
=======
Obrigatório para exposição segura à Internet (HTTPS). Escolhe uma opção:
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e

| Opção | Ideal para |
|---|---|
| [Nginx Proxy Manager](https://nginxproxymanager.com/) | Interface gráfica, SSL fácil via Let's Encrypt |
| [Traefik](https://traefik.io/) | Configuração via labels Docker, utilizadores avançados |
<<<<<<< HEAD
| [Caddy](https://caddyserver.com/) | Config mínima, HTTPS automático por defeito |
=======
| [Caddy](https://caddyserver.com/) | Configuração mínima, HTTPS automático |
>>>>>>> e4df3824ba0e8ee613f2f1cc8a6c5ea5ae870c8e
