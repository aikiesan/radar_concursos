# Ferramentas do AI Job Search

Cópias sem alteração de `tools/` do [ai-job-search-dev/ai-job-search](https://github.com/ai-job-search-dev/ai-job-search), sob a licença MIT (ver `LICENSE` nesta pasta).

| Arquivo | Uso aqui |
|---|---|
| `posting_guard.py` | portão de integridade: limpa e examina o texto de cada edital antes da nota |
| `fetch_page.py`, `page_decode.py`, `robots_check.py` | baixar um edital com cabeçalhos de navegador, respeitando o `robots.txt`, quando a busca comum falha |
| `job_key.py` | chave estável de deduplicação (empresa + título) |
| `security_guards.py` | dependência das anteriores |

Exemplo:
```bash
python tools/ajs/posting_guard.py --text --json <<'EOF'
texto do edital
EOF
```
