# Radar Concursos

Painel semanal de vagas de professor, pesquisador e cargo público no **estado de São Paulo** (mais outros estados e exterior quando o ajuste é alto), pontuadas contra um currículo pelo método do [AI Job Search](https://github.com/ai-job-search-dev/ai-job-search).

**Painel:** https://aikiesan.github.io/radar_concursos/

## Como funciona
1. Todo domingo às 20h30 (horário de Brasília) uma rotina do Claude Code na nuvem procura editais, abre cada um, passa o texto pelo portão de integridade e pontua a vaga (ver [`metodo/avaliacao.md`](metodo/avaliacao.md)).
2. A rotina grava `data/radar_vagas_AAAA-MM-DD.json` numa branch `claude/radar-AAAA-MM-DD` e envia.
3. O workflow [`pages.yml`](.github/workflows/pages.yml) valida o relatório com `tools/atualizar_indice.py`, leva a branch para a `main` e publica o painel no GitHub Pages.

A situação de cada vaga (interessado, preparando, inscrito) e as notas que você escrever no painel ficam salvas **só no seu navegador**; nada disso volta para o repositório.

## Estrutura
| Caminho | Conteúdo |
|---|---|
| `index.html` | o painel (arquivo único, sem build) |
| `data/` | um relatório JSON por semana |
| `metodo/avaliacao.md` | portões, dimensões, pesos e formato do JSON |
| `tools/atualizar_indice.py` | valida os relatórios e gera `data/index.json` |
| `tools/ajs/` | ferramentas copiadas do AI Job Search (MIT) |

## Privacidade
Este repositório é público. O perfil detalhado usado na pontuação fica num arquivo privado no Google Drive, fora daqui. Os relatórios trazem só dados públicos dos editais e uma avaliação curta de ajuste.

## Ver localmente
```bash
python -m http.server 8000
```
e abra http://localhost:8000.
