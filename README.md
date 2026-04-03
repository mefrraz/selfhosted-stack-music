<div align="center">

# 🎵 Self-Hosted Music Stack

**A personal, high-fidelity music infrastructure — fully self-hosted and Docker-ready.**

[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Navidrome](https://img.shields.io/badge/Navidrome-Subsonic%20API-F2711C?logo=musicbrainz&logoColor=white)](https://www.navidrome.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

🇬🇧 English | [🇵🇹 Português](#-português)

</div>

---

## 🇬🇧 English

### ✨ Features

| | Feature |
|---|---|
| 🎧 | Stream your entire music library via any Subsonic-compatible client |
| 📥 | Automated FLAC/MP3 acquisition with full ID3v2 tagging |
| 🎤 | Mass lyrics sync embedded directly into audio files |
| 📻 | Radio station automation via Radio-Browser API |
| 🐳 | Fully containerized — runs anywhere Docker runs |

---

### 🧩 Stack Overview

```
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
```

---

### 🚀 Quick Start

#### Prerequisites

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

```bash
docker compose up -d
```

---

### 🧱 Components

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

Required for secure WAN exposure (HTTPS). Choose one:

| Option | Best for |
|---|---|
| [Nginx Proxy Manager](https://nginxproxymanager.com/) | GUI-based, easy SSL via Let's Encrypt |
| [Traefik](https://traefik.io/) | Docker label-based config, power users |
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
```

---

### 🚀 Início Rápido

#### Pré-requisitos

- Docker & Docker Compose instalados
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

```bash
docker compose up -d
```

---

### 🧱 Componentes

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
pip install requests

# Executar
python3 navidrome-radio.py
```

---

### ⚙️ Variáveis de Ambiente

| Variável | Serviço | Descrição | Valor Sugerido |
|---|---|---|---|
| `PUID` | Deemix | ID do utilizador no Host para posse de ficheiros | `1000` |
| `PGID` | Deemix | ID do grupo no Host para posse de ficheiros | `1000` |
| `UMASK_SET` | Deemix | Máscara de permissões (`022` = 644/755) | `022` |
| `ND_LOGLEVEL` | Navidrome | Nível de detalhe dos logs (`info`, `debug`) | `info` |
| `ND_UI_VAMP_THEME` | Navidrome | Tema padrão da interface web | `dark` |

---

### 🌐 Acesso Remoto (Reverse Proxy)

Obrigatório para exposição segura à Internet (HTTPS). Escolhe uma opção:

| Opção | Ideal para |
|---|---|
| [Nginx Proxy Manager](https://nginxproxymanager.com/) | Interface gráfica, SSL fácil via Let's Encrypt |
| [Traefik](https://traefik.io/) | Configuração via labels Docker, utilizadores avançados |
| [Caddy](https://caddyserver.com/) | Configuração mínima, HTTPS automático |
