# Hammerfy — Project Context

> Cole este arquivo no início de cada sessão com a IA para restaurar o contexto completo do projeto.

---

## O que é o Hammerfy

Hammerfy é um manager e futuro substituto ao instalador oficial do **Hammer++** (editor de mapas para a Source Engine da Valve).

O nome vem de:
- **Hammer** — o software Hammer / Hammer++ da Valve
- **fy** — sufixo inspirado no "Rectify", ferramenta de tema escuro do Windows 11

O projeto nasce como evolução do **Darker++**, ferramenta anterior do mesmo autor que aplicava tema escuro ao Hammer++ alterando `.dll` e o tema global do sistema operacional. O Hammerfy resolve as limitações do Darker++ e vai muito além.

**Repositório:** `kenned-candido/darkerplusplus` (mesmo repo do Darker++)

---

## Contexto do Darker++ (projeto anterior)

- Alterava `.dll` do Hammer++ para manter ícones em tema escuro
- Mudava o tema do sistema operacional inteiro (problema — usuário nem sempre quer isso)
- Funcional mas ineficiente e limitado
- Branch `legacy/darker++` preservará o projeto original quando o Hammerfy virar `main`

---

## Estratégia de Repositório

| Branch | Conteúdo |
|---|---|
| `main` | Darker++ atual (preserva estrelas e histórico) |
| `hammerfy-dev` | Desenvolvimento ativo do Hammerfy |
| `legacy/darker++` | Arquivo do Darker++ após o Hammerfy ir para main |

Quando o Hammerfy estiver pronto para release, o Darker++ é arquivado em `legacy/darker++` e o Hammerfy assume a `main`. Isso preserva estrelas, forks e reputação do repositório.

---

## Stack Técnica Final

| Componente | Tecnologia | Motivo |
|---|---|---|
| Linguagem | Python 3.12+ | Backend sólido, bom ecossistema Windows |
| Interface | PySide6 | Binding oficial Qt, LGPL, open-source friendly, alta performance |
| Windows API | `winreg` · `subprocess` · `ctypes` | Manipulação de registro, processos e DLLs |
| Empacotamento | PyInstaller | Gera `.exe` standalone, usuário não precisa instalar Python |
| Versionamento | Git + GitHub | Open-source, releases organizados |
| Distribuição | GitHub Releases | Gratuito, open-source |

**Por que PySide6 e não PyQt6:** Licença LGPL (mais limpa para open-source). API praticamente idêntica ao PyQt6.

**Por que não Electron:** Pesado, alto consumo de RAM/CPU (ex: Discord).

**Por que não Tauri:** Exige Rust, curva de aprendizado alta demais para o momento.

**Por que não PyWebview/CustomTkinter/Flet:** Limitados para a complexidade e personalização que o Hammerfy exige.

---

## O que o Hammer++ permite modificar

- Idioma (via arquivos de localização)
- Ícones (via `.dll`)
- Imagens e banners internos
- Temas
- Título da janela

---

## Plano de Fases

### Fase 1 — MVP: Library Manager ← FASE ATUAL
O core do projeto. Gerenciamento completo das instalações do Hammer++.

- [ ] Interface principal com grid de ferramentas (estilo Steam, mas para Hammer++)
- [ ] Detecção automática da Steam e jogos instalados
- [ ] Listagem de todas as versões do Hammer++ disponíveis por jogo
- [ ] Ações por ferramenta: Instalar, Desinstalar, Abrir, Abrir pasta, Atualizar
- [ ] Painel lateral de detalhes por ferramenta selecionada
- [ ] Sidebar com filtros: Todos · Instalados · Disponíveis · Com atualização
- [ ] Busca por nome
- [ ] Sistema de versionamento: versão instalada vs versão disponível
- [ ] Empacotamento em `.exe` funcional via PyInstaller

### Fase 2 — Tema Escuro Nativo
Resolver o problema central do Darker++ de forma elegante e cirúrgica.

- [ ] Aplicar tema escuro somente no processo do Hammer++ (sem alterar tema do sistema)
- [ ] Substituição das `.dll` de ícones integrada ao manager
- [ ] Preview do tema antes de aplicar
- [ ] Opção de reverter para o padrão

### Fase 3 — Personalização Avançada
O diferencial real do Hammerfy.

- [ ] Troca de cor dos ícones do Hammer++
- [ ] Troca do título da janela
- [ ] Seleção de idioma
- [ ] Troca de banners e imagens internas
- [ ] Perfis de personalização — salvar e carregar configs por jogo

### Fase 4 — Substituto ao Instalador Oficial
Hammerfy como instalador completo, eliminando a necessidade do instalador original.

- [ ] Download direto do Hammer++ mais recente por jogo
- [ ] Verificação de integridade dos arquivos
- [ ] Instalação silenciosa
- [ ] Migração automática de instalações existentes

### Fase 5 — Polimento e Comunidade

- [ ] Auto-updater do próprio Hammerfy
- [ ] Suporte a temas da comunidade (importar/exportar)
- [ ] Documentação completa
- [ ] Página de releases organizada no GitHub

---

## Design da Interface (Fase 1)

Referência visual: **Steam Library**, mas para abrir Hammer++ ao invés de jogos.

Estrutura da janela principal:
- **Sidebar esquerda** — logo, navegação (All tools / Installed / Available / Updates / Settings)
- **Grid central** — cards por jogo com banner colorido, status, versão e ações rápidas
- **Painel direito** — detalhes da ferramenta selecionada (info, path, customização, ações completas)
- **Topbar** — título da seção, contador, busca, toggle grid/lista

Tema: escuro por padrão (`#1a1a1a` base, `#e05c20` accent laranja).

---

## Regras do Projeto

1. **Evoluir por fases sem pular etapas** — cada fase só começa quando a anterior estiver completa
2. **Gratuito e open-source** — sem exceções
3. **Performance primeiro** — nada de soluções pesadas
4. **O usuário não altera o sistema todo** — qualquer modificação no Windows deve ser cirúrgica e reversível

---

## Status Atual

- [x] Conceito definido
- [x] Stack técnica definida
- [x] Plano de fases definido
- [x] Design do MVP conceituado (mockup criado)
- [x] CONTEXT.md criado
- [ ] Repositório configurado (branch `hammerfy-dev` criado)
- [ ] Estrutura inicial do projeto criada
- [ ] Desenvolvimento da Fase 1 iniciado
