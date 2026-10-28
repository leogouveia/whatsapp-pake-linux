# Publicar uma release

[← README](../README.md)

## O que a automação faz

Uma tag `v<versão>` ou uma execução manual do workflow **Build and publish Linux release**, indicando uma tag existente, executa quatro builds:

1. Ubuntu 22.04 → DEB.
2. Ubuntu 22.04 → AppImage.
3. Fedora 44 → RPM.
4. Arch atualizado → `.pkg.tar.zst`.

Os jobs enviam seus arquivos como artefatos temporários do Actions. O job final depende do sucesso de todos, exige exatamente um arquivo de cada formato, cria um arquivo dos fontes completos e gera `SHA256SUMS`.

Ele cria a release como rascunho, envia os arquivos e só então a publica. Uma falha de qualquer build impede a publicação final. Não reescreve uma release já publicada. Para corrigir uma versão publicada, incremente a versão e crie outra tag.

A publicação usa `GITHUB_TOKEN` com `contents: write` somente no job final; não exige um token pessoal nos secrets. O código da aplicação não contém token do GitHub.

## Checklist do mantenedor

1. Atualize a versão nos três arquivos: `package.json`, `src-tauri/Cargo.toml` e `src-tauri/tauri.conf.json`.
2. Atualize os lockfiles: `npm install --package-lock-only` e `cargo metadata --manifest-path src-tauri/Cargo.toml --format-version 1 --filter-platform x86_64-unknown-linux-gnu`.
3. Atualize `CHANGELOG.md` e `docs/RELEASE-NOTES.md` com o que mudou e o que foi validado.
4. Execute `npm run validate` e pelo menos o build da sua distro.
5. Confira notificações, X/ocultar/reabrir, DevTools e a origem dos pacotes.
6. Faça commit e envie a branch.

```bash
git tag -a v1.0.1 -m "WhatsApp Pake Linux 1.0.1"
git push origin main
git push origin v1.0.1
```

Acompanhe:

```bash
gh run list --workflow release.yml
gh run watch ID_DA_EXECUCAO
gh release view v1.0.1
```

Se um build falhar, leia seus logs antes de repetir. Uma execução manual pode reconstruir uma tag ainda sem release publicada. Não remova validações ou publique apenas um subconjunto para esconder falhas.

## Atualizar Pake ou dependências

A origem exata está em [PROVENANCE.md](PROVENANCE.md). Este projeto é um snapshot adaptado, não um wrapper que baixa automaticamente o Pake mais novo.

Ao atualizar notify-rust ou Tao, confira se o problema foi resolvido upstream antes de reaplicar patches. Atualize o código em `vendor/`, seus avisos de licença e os diffs em `patches/`; revise a resolução no Cargo.lock. Não execute um `cargo update` amplo sem revisar a mudança de escopo.

Para o patch de janela, a mudança local é parcial: atualizar todo o Tao/Tauri pode ser preferível quando a nova versão for compatível e validada. Teste especialmente GNOME/Wayland, ocultar/reabrir e fullscreen.

## Limites dos builds automáticos

A automação prova compilação e geração dos pacotes. Não comprova login, entrega de mensagem, reprodução de mídia ou todos os comportamentos de janela em um desktop real. Registre os testes manuais de cada release honestamente.
