# Build do zero

[← README](../README.md)

## Pré-requisitos comuns

- Linux x86_64, Git, Python 3 e ferramentas nativas de compilação.
- Rust estável via [rustup](https://rustup.rs/) ou os pacotes da distro.
- Node.js 22 e npm para a CLI do Tauri. O pacote Arch pode ser gerado só com Cargo e Python.
- Internet no primeiro build para baixar as dependências fixadas nos lockfiles.

Os patches já estão aplicados em `vendor/`. O Cargo os seleciona por `[patch.crates-io]`. Não modificar o cache global de crates nem executar a CLI original do Pake: isso pode regenerar configurações e remover as correções deste projeto.

## Fedora 44: RPM

```bash
sudo dnf install git gcc gcc-c++ make pkgconf-pkg-config python3 curl wget file \
  openssl-devel webkit2gtk4.1-devel gtk3-devel libappindicator-gtk3-devel \
  librsvg2-devel libxdo-devel rpm-build
```

Instale Rust/rustup e Node.js 22 caso ainda não estejam disponíveis. Depois:

```bash
git clone https://github.com/leogouveia/whatsapp-pake-linux.git
cd whatsapp-pake-linux
npm ci
BUILD_FLAVOR=fedora44 bash scripts/build.sh rpm
```

## Ubuntu 22.04: DEB e AppImage

```bash
sudo apt-get update
sudo apt-get install build-essential git python3 curl wget file \
  libwebkit2gtk-4.1-dev libgtk-3-dev libxdo-dev libssl-dev \
  libayatana-appindicator3-dev librsvg2-dev patchelf squashfs-tools libfuse2 \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-libav
```

Com Rust e Node.js instalados:

```bash
npm ci
BUILD_FLAVOR=ubuntu22.04 bash scripts/build.sh deb
APPIMAGE_EXTRACT_AND_RUN=1 NO_STRIP=1 BUILD_FLAVOR=ubuntu22.04 bash scripts/build.sh appimage
```

AppImage inclui o framework multimídia para suportar os recursos de áudio/vídeo do WhatsApp. Seu tamanho será maior que o dos pacotes nativos. Nem todo codec ou integração pode ser validado automaticamente.

## Arch / CachyOS: pacote pacman

```bash
sudo pacman -Syu --needed base-devel git rust cargo python webkit2gtk-4.1 gtk3 \
  libappindicator-gtk3 librsvg xdotool openssl file libarchive zstd
bash scripts/build.sh arch
```

Saída: `out/whatsapp-<versão>-1-x86_64.pkg.tar.zst`. A receita não exige root e não instala o pacote. `bsdtar` normaliza o proprietário dos arquivos no arquivo gerado para root. O pacote usa `.PKGINFO`; ele não tem assinatura de um repositório de distribuição.

## Apenas o executável

```bash
cd src-tauri
cargo build --locked --release --features notification-diagnostics
```

O Cargo gera `target/release/pake`. O nome final de distribuição é `pake-whatsapp`. Para um teste manual, copie-o para uma pasta junto ao recurso `png/whatsapp_512.png`, preservando o caminho relativo. Não execute simultaneamente com uma instalação que usa a mesma identidade/perfil.

`--release` gera um binário otimizado. A feature `notification-diagnostics` mantém DevTools e seu menu habilitados; não é necessário um build enorme e sem otimização para inspecionar a página.

## Versões e verificação

```bash
npm run validate
cargo tree --manifest-path src-tauri/Cargo.toml -i notify-rust
cargo tree --manifest-path src-tauri/Cargo.toml -i tao
```

Os dois últimos comandos devem apontar para `vendor/`. Preserve `Cargo.lock` e `package-lock.json`. O projeto usa o compilador estável disponível no ambiente; lockfiles não tornam o build idêntico byte a byte quando compilador, bibliotecas ou sistema mudam.

Para builds sem rede, depois de preencher os caches, use `cargo build --offline --locked --release --features notification-diagnostics`. O empacotamento AppImage pode baixar ferramentas adicionais no primeiro uso.

## Ambientes e compatibilidade

| Artefato | Ambiente de compilação da release | Validação visual conhecida |
|---|---|---|
| RPM | Contêiner Fedora 44 | Ainda requer teste no Fedora/desktop de destino |
| DEB | Runner Ubuntu 22.04 | Ainda requer teste no sistema de destino |
| AppImage | Runner Ubuntu 22.04 | Ainda requer teste no sistema de destino |
| Arch | Contêiner Arch atualizado | Versão local anterior validada em CachyOS/GNOME 51.1/Wayland |

A base Ubuntu mais antiga reduz o requisito mínimo de glibc para DEB/AppImage. AppImage não elimina todos os requisitos do host. RPM é compilado no Fedora; o pacote Arch é compilado no Arch. Converter um arquivo `.pkg.tar.zst` em RPM não substitui esse processo.

As imagens de distro e Rust estável recebem atualizações; não prometemos reproduzir hashes de builds passados. Releases guardam os binários e hashes gerados para permitir reutilizá-los após reinstalação.

## Contêineres

O workflow `.github/workflows/release.yml` é a receita executável dos ambientes. Para repetir localmente com Podman, monte o clone em `/work` usando `-v "$PWD:/work:Z" -w /work`, escolha `fedora:44` ou `archlinux:base-devel`, instale as mesmas dependências e execute o script correspondente. O sufixo `:Z` é necessário em muitos hosts Fedora com SELinux.

Compilar não testa a interface gráfica. Execute o instalador ou binário no desktop real e siga [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
