#!/usr/bin/env python3
"""Valida os relatórios semanais e gera data/index.json para o painel.

Uso:
    python tools/atualizar_indice.py                # valida data/ e grava data/index.json
    python tools/atualizar_indice.py --out site/data  # grava o índice (e cópias) em outra pasta

Sai com código 1 se algum relatório estiver malformado, para o GitHub Actions
não publicar um painel quebrado.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NAME = re.compile(r"^radar_vagas_(\d{4}-\d{2}-\d{2})(?:_([a-z]))?\.json$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GATE = {"eleg": {"PASS", "FAIL", "NAO_VERIFICADO"}, "idioma": {"PASS", "FLAG", "FAIL"}, "local": {"PASS", "FLAG", "FAIL"}}
DIMS = ("tecnica", "experiencia", "institucional", "carreira")
TIPOS = {"efetivo", "pesquisador", "visitante_temporario", "postdoc", "fomento", "cargo_publico", "docente_privado", "setor_privado"}


def check(path: Path) -> list[str]:
    errs: list[str] = []
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"{path.name}: JSON inválido ({e})"]
    vagas = d.get("vagas")
    if not isinstance(vagas, list):
        return [f"{path.name}: falta a lista 'vagas'"]
    if not DATE.match(str(d.get("gerado_em", ""))):
        errs.append(f"{path.name}: 'gerado_em' deve ser AAAA-MM-DD")
    seen: set[str] = set()
    v4 = int(d.get("versao", 0) or 0) >= 4
    for i, v in enumerate(vagas):
        where = f"{path.name} vaga {i} ({v.get('id', '?')})"
        if not v.get("id") or not v.get("titulo"):
            errs.append(f"{where}: precisa de 'id' e 'titulo'")
        if v.get("id") in seen:
            errs.append(f"{where}: id repetido")
        seen.add(v.get("id"))
        for k in ("inscricoes_ate", "prazo_isencao", "inscricoes_inicio", "primeiro_relato", "ultima_verificacao"):
            if v.get(k) is not None and not DATE.match(str(v[k])):
                errs.append(f"{where}: '{k}' deve ser AAAA-MM-DD ou null")
        if not v4:
            continue
        if v.get("tipo") not in TIPOS:
            errs.append(f"{where}: tipo '{v.get('tipo')}' desconhecido")
        nota = v.get("nota")
        if nota is not None and not (isinstance(nota, (int, float)) and 0 <= nota <= 100):
            errs.append(f"{where}: 'nota' fora de 0-100")
        dims = v.get("dimensoes")
        if dims is not None:
            for k in DIMS:
                x = dims.get(k)
                if x is not None and not (isinstance(x, (int, float)) and 0 <= x <= 100):
                    errs.append(f"{where}: dimensão '{k}' fora de 0-100")
        p = v.get("portoes") or {}
        for k, ok in GATE.items():
            if k in p and p[k] not in ok:
                errs.append(f"{where}: portão '{k}' = '{p[k]}' inválido")
        if v.get("link") and not str(v["link"]).startswith(("http://", "https://")):
            errs.append(f"{where}: link deve começar com http")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DATA, help="pasta onde gravar index.json (e copiar os relatórios, se não for data/)")
    a = ap.parse_args()
    files = sorted((p for p in DATA.glob("radar_vagas_*.json") if NAME.match(p.name)), key=lambda p: p.name, reverse=True)
    if not files:
        print("nenhum relatório em data/", file=sys.stderr)
        return 1
    errs = [e for p in files for e in check(p)]
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return 1
    out = a.out if a.out.is_absolute() else (Path.cwd() / a.out)
    out.mkdir(parents=True, exist_ok=True)
    if out.resolve() != DATA.resolve():
        for p in files:
            shutil.copy2(p, out / p.name)
    idx = {"relatorios": [{"arquivo": p.name, "data": NAME.match(p.name).group(1)} for p in files]}
    (out / "index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(files)} relatório(s) válidos; mais recente: {files[0].name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
