---
{
  "schema": "wellmanifest.docs/document/v1",
  "id": "internal-dependencies",
  "kind": "information",
  "version": 1,
  "title": "Aktualizacja i kontrola zależności wewnętrznych",
  "status": "implemented",
  "owner": "semcod/testless",
  "created": "2026-09-06",
  "updated": "2026-09-06",
  "review_after": "2026-09-13",
  "source_revision": "2a847ef3f3ae4a4e5164f567bdb21944e5bde6be",
  "affected_repositories": [
    "semcod/testless"
  ],
  "evidence": [
    "https://github.com/semcod/testless/blob/2a847ef3f3ae4a4e5164f567bdb21944e5bde6be/pyproject.toml",
    "https://pypi.org/project/goal/2.2.0/",
    "https://docs.astral.sh/uv/concepts/projects/dependencies/",
    "https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference"
  ]
}
---

# Aktualizacja i kontrola zależności wewnętrznych

<!-- docs:section purpose -->
## Cel

Utrzymywać aktualne, przetestowane zależności projektu `semcod/testless` przy zachowaniu Pythona 3.11 jako minimalnej wersji aplikacji.

<!-- docs:section scope -->
## Zakres

Właścicielem lockfile i CI jest `semcod/testless`. Katalog [.github/internal-dependencies.json](../../.github/internal-dependencies.json) obejmuje pięć jawnie wskazanych dystrybucji PyPI: costs, goal, pfix, clickmd i code2llm. Audyt sprawdza te z nich, które występują w uv.lock. Nie obejmuje dowolnego pakietu tylko na podstawie nazwy organizacji.

<!-- docs:section evidence -->
## Dowody

Przed zmianą wersja źródłowa wskazana w metadanych miała starsze zależności i nie miała workflow testów lockfile ani audytu aktualności. W odczycie PyPI z 2026-09-06 aktualnymi stabilnymi wersjami były costs 0.2.0, goal 2.2.0, pfix 0.1.79 i clickmd 1.1.15; te wersje zapisano w uv.lock.

Lokalne testy zatwierdzanego lockfile: 47 testów przeszło na Pythonie 3.11 oraz 3.13. Wyniki publikacji i kolejnych kontroli są dostępne w [GitHub Actions](https://github.com/semcod/testless/actions).

<!-- docs:section content -->
## Obsługa

Goal jest narzędziem automatyzacji, bez importów w kodzie aplikacji. Grupa `automation` wymaga Pythona >=3.12 i nie jest domyślnie instalowana z aplikacją ani dodatkiem `dev`. Zastosowano [oddzielny zakres Pythona grupy uv](https://docs.astral.sh/uv/concepts/projects/dependencies/#group-requires-python).

```bash
uv sync --locked --extra dev --python 3.11
uv run --no-sync python -m pytest -q
```

Dependabot codziennie proponuje aktualizację wewnętrznych pakietów w jednym PR. Testy uruchamiają zatwierdzony lockfile na Pythonie 3.11 i 3.13. Osobny workflow codziennie oraz po zmianie zależności w PR porównuje lockfile z najwyższymi stabilnymi wydaniami w katalogu; zachowuje raport jako artefakt. Obie automatyzacje można uruchomić ręcznie.

Ręczny audyt używa grupy narzędziowej:

```bash
uv run --locked --group automation --python 3.12 goal dependencies --catalog .github/internal-dependencies.json --check
```

Aktualizacja wybranych pakietów:

```bash
uv lock --upgrade-package costs --upgrade-package goal --upgrade-package pfix --upgrade-package clickmd --upgrade-package code2llm
```

Po aktualizacji uruchom testy, opublikuj PR, a po jego sprawdzeniu i scaleniu zsynchronizuj środowisko. CI kontroluje też położenie i metadane dokumentacji według wellmanifest/docs 0.1.1, przypiętego do `ebe7501063ef4f3e63ded610c2d3183010ca636e` w `.governance/docs.json`.

<!-- docs:section limitations -->
## Ograniczenia

Ograniczenie `>=` dopuszcza nowszą wersję, lecz nie zmienia istniejącego środowiska. `uv sync --locked` odtwarza wersje z lockfile. Codzienny PR nie jest automatycznie scalany ani wdrażany. Opóźnienie zależy od harmonogramu, testów i procesu publikacji.

Checker w CI jest przypięty do Goal 2.2.0. Jego aktualizację trzeba wykonać jawnie. Audyt tej wersji porównuje stabilne wersje x.y.z i nie jest pełnym resolverem wszystkich formatów wersji ani kontrolą pochodzenia każdego pakietu. Dokładne przypięcie standardu dokumentacji podlega osobnej, sprawdzanej aktualizacji.

<!-- docs:section next_actions -->
## Utrzymanie

Sprawdzaj nieudane harmonogramy i zaległe PR-y. Nową dystrybucję dodaj do katalogu dopiero po potwierdzeniu jej właściciela i sposobu wersjonowania. Wyniki przekrojowe rozwijaj w [kanonicznym raporcie subactor/docs](https://github.com/subactor/docs/blob/main/architecture/analysis/internal-dependencies.md). Zwiększ wersję tego dokumentu po zmianie mechanizmu.
