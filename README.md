# README: SQLite Kvíz

## Popis
Tento program načítá otázky z databáze SQLite a spouští kvíz, ve kterém uživatel odpovídá na otázky s výběrem odpovědí.

## Požadavky
- **Python**
- **SQLite3 knihovna** (součást standardní knihovny Pythonu)
- **Databázový soubor** `Pro3.db`, který obsahuje tabulku `Quiz` se sloupci **`(vytvořený pomocí DB Browser [SQLite])`**:
  - `Otazka` *(TEXT)* – Text otázky
  - `Odpoved1`, `Odpoved2`, `Odpoved3`, `Odpoved4` *(TEXT)* – Možnosti odpovědí
  - `SpravnaOd` *(INTEGER)* – Index správné odpovědi *(0–3)*

## Použití
1. Ujistěte se, že máte soubor **`Pro3.db`** ve stejném adresáři jako skript.
2. Ujistěte se, že jste zapnuli konzoli.
3. Otevřete si port na adrese http://localhost:1000/
4. Program načte otázky z databáze a zobrazí je na serveru po kliknutí na tlačítko.
5. Uživatel vybírá číslo odpovědi *(1–4).*
6. Po odpovědi se zobrazí výsledek a po dokončení všech otázek **celkové skóre**.

## Poznámky
- `**Databázový soubor**` musí být ve správném formátu.
- **`Složka PredelanejProjektZCPP`** je výpomoc na kterou pak navazuji spojením projektů dohromady. jelikož jsem ten předchozí projekt dělal v CPP

