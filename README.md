# Self-Hosted Music Stack Configuration

> 🇬🇧 [English](#english) | 🇵🇹 [Português](#português)

---

## English

### Technical Overview

A high-performance orchestration for a personal music infrastructure. This stack focuses on automated asset acquisition, metadata synchronization, and high-fidelity streaming.

---

### Components and Logic

#### 1. Navidrome (Core Engine)

A Subsonic-compliant music server written in Go. It handles music indexing and serves the API for web and mobile clients.

- **Themes:** Supports various built-in themes (e.g., Dracula, Nord, Dark).
- **Clients:** Compatible with any Subsonic client. Recommended: [Feishin](https://github.com/jeffvli/feishin) (Desktop) and [Substreamer](https://substreamerapp.com/) (Mobile).

#### 2. Deemix (Bambanah Edition)

The primary tool for audio retrieval and ID3v2 tagging.

- **ARL (Authentication):** Requires a Deezer ARL token.
  - **How to obtain:** Login to Deezer on a desktop browser → open Developer Tools (`F12`) → Application → Cookies → copy the `arl` cookie value.
- **Workflow:** Configured to download FLAC/MP3 files.
  - > ⚠️ Integrated lyrics download is disabled due to API instability. Use **LRCGET** for post-processing.

#### 3. LRCGET (Lyrics Management)

Utility for mass-downloading and synchronizing LRC lyrics via the [LRCLIB](https://lrclib.net/) service.

- **Integration:** Must be configured to embed lyrics directly into the audio containers (ID3v2 tags) for seamless Navidrome compatibility.

#### 4. Radio Automation

Powered by `navidrome-radio.py`. This script interfaces with the [Radio-Browser API](https://www.radio-browser.info/).

- **Features:** Search by station name, genre, or country; pagination support; duplicate detection.
- **Operation:** Performs direct SQL injection into the `navidrome.db` SQLite file.

---

### Docker Specification

#### Variable Mapping (Environment)

| Variable | Service | Description | Default |
|---|---|---|---|
| `PUID` | Deemix | Host User ID for file ownership | `1000` |
| `PGID` | Deemix | Host Group ID for file ownership | `1000` |
| `UMASK_SET` | Deemix | File permission mask (`022` = 644/755) | `022` |
| `ND_LOGLEVEL` | Navidrome | Logging verbosity (`info`, `debug`, `error`) | `info` |
| `ND_UI_VAMP_THEME` | Navidrome | Default UI theme | `dark` |

#### Remote Access (Reverse Proxy)

Mandatory for WAN exposure (HTTPS). Options:

- **[Nginx Proxy Manager](https://nginxproxymanager.com/):** GUI-based, easy SSL management.
- **[Traefik](https://traefik.io/):** Infrastructure-as-code alternative.
- **[Caddy](https://caddyserver.com/):** Minimalist web server with automatic HTTPS by default.

---

### Radio Installation Commands

```bash
# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies and run script
pip install requests
python3 navidrome-radio.py
```

---
---

## Português

### Visão Geral Técnica

Orquestração de alto desempenho para uma infraestrutura de música pessoal. Esta *stack* foca-se na aquisição automatizada de ativos, sincronização de metadados e streaming de alta fidelidade.

---

### Componentes e Lógica do Sistema

#### 1. Navidrome (Motor Central)

Servidor de música compatível com Subsonic escrito em Go. Gere a indexação da biblioteca e providencia a API para clientes web e móveis.

- **Temas:** Suporta diversos temas nativos (ex: Dracula, Nord, Dark, Midday).
- **Clientes:** Compatível com qualquer cliente Subsonic. Recomendados: [Feishin](https://github.com/jeffvli/feishin) (Desktop) e [Substreamer](https://substreamerapp.com/) (Mobile).

#### 2. Deemix (Versão Bambanah)

Ferramenta primária para aquisição de áudio e etiquetagem ID3v2.

- **ARL (Autenticação):** O token ARL é obrigatório para autenticação com o Deezer.
  - **Como obter:** Faça login no Deezer num browser desktop → abra as Ferramentas de Programador (`F12`) → Application → Cookies → copie o valor do cookie `arl`.
- **Fluxo de Trabalho:** Configurado para descarregar ficheiros FLAC/MP3.
  - > ⚠️ A opção de download de letras nativa deve ser ignorada por instabilidade. Utilize o **LRCGET** para embutir letras após o download.

#### 3. LRCGET (Gestão de Letras)

Utilitário para download em massa e sincronização de letras via serviço [LRCLIB](https://lrclib.net/).

- **Integração:** Deve ser configurado para *"Juntar letras aos ficheiros de música"* (Embed). Isto garante que o Navidrome as detete via tags internas sem necessidade de ficheiros `.lrc` externos.

#### 4. Automação de Rádios

Gerido pelo script `navidrome-radio.py`, que utiliza a [API Radio-Browser](https://www.radio-browser.info/).

- **Funcionalidades:** Pesquisa avançada por nome (ex: Comercial, RFM), género (jazz, rock) ou país; suporte para paginação de resultados; deteção de duplicados.
- **Funcionamento:** O script realiza injeção direta de dados no ficheiro SQLite `navidrome.db`, não requerendo o reinício do contentor Navidrome.

---

### Especificação Docker

#### Tabela de Variáveis (Ambiente)

| Variável | Serviço | Descrição | Valor Sugerido |
|---|---|---|---|
| `PUID` | Deemix | ID do utilizador no Host para posse de ficheiros | `1000` |
| `PGID` | Deemix | ID do grupo no Host para posse de ficheiros | `1000` |
| `UMASK_SET` | Deemix | Máscara de permissões (`022` = 644/755) | `022` |
| `ND_LOGLEVEL` | Navidrome | Nível de detalhe dos logs (`info`, `debug`) | `info` |
| `ND_UI_VAMP_THEME` | Navidrome | Tema padrão da interface web | `dark` |

#### Acesso Remoto (Reverse Proxy)

Obrigatório para exposição segura à Internet (HTTPS). Opções recomendadas:

- **[Nginx Proxy Manager](https://nginxproxymanager.com/):** Interface gráfica para gestão de domínios e certificados SSL (Let's Encrypt).
- **[Traefik](https://traefik.io/):** Recomendado para quem prefere configuração via labels de Docker.
- **[Caddy](https://caddyserver.com/):** Servidor web minimalista com HTTPS automático por defeito.

---

### Comandos para Instalação de Rádios

```bash
# Criar ambiente virtual Python
python3 -m venv venv
source venv/bin/activate

# Instalar dependências e correr script
pip install requests
python3 navidrome-radio.py
```