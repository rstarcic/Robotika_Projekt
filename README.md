# 📅 **Automatski raspored predavanja** - Greedy i Hill Climbing Optimizacija
---
 **Fakultet**: Fakultet informatike u Puli  
 **Studij**: Informatika (diplomski studij)
 **Kolegij**: Robotika  
 **Mentor** : doc. dr. sc. Ivan Lorencin
 **Studenti**: Elvis Starić, Roberta Starčić
 
 
## 🎯 Cilj projekta

Razviti sustav koji automatski generira **tjedni raspored predavanja i vježbi** za više godina studija, uz uvažavanje pedagoških i organizacijskih pravila. Sustav omogućuje:

- Planiranje akademskog kalendara
- Automatizaciju složenih rasporeda u obrazovnim ustanovama
- Simulaciju i evaluaciju alternativnih rješenja

Projekt kombinira **Greedy algoritam** za brzo generiranje valjanog rasporeda i **Hill Climbing optimizaciju** za njegovo poboljšanje.

---

## 📌 Opis problema

### 🔧 Problem:
- Zakazivanje predavanja i vježbi za više godina studija
- Mnoštvo ograničenja: dostupnost profesora, kapacitet učionica, kolizije, hijerarhija predavanja/vježbi, zajednički termini za izborne kolegije

### 💡 Rješenje:
- **Greedy pristup** za brzo zakazivanje osnovnih termina
- **Hill Climbing optimizacija** za prilagodbu i poboljšanje rasporeda

--- 
## 🧠 Algoritamski pristup

### Greedy algoritam:
- Zakazuje svaki kolegij u prvi slobodni odgovarajući termin
- Poštuje: dostupnost profesora, tip učionice, zauzeće termina

### Hill Climbing:
- Optimizira raspored na temelju više kriterija:
  - Vježbe se zakazuju nakon predavanja
  - Preferiraju se jutarnji i raniji tjedni termini
  - Penaliziraju se večernji termini i nepoželjne kombinacije
- Poboljšava evaluacijsku funkciju rasporeda

## Pravila zakazivanja

✅ Nema kolizija među profesorima  
✅ Vježbe slijede pripadajuća predavanja  
✅ Laboratorijske vježbe idu isključivo u laboratorije  
✅ Izborni kolegiji imaju zajednički termin za sve godine  
✅ Preferiraju se jutarnji i rani tjedni termini  
✅ Izborni kolegiji zakazuju se isključivo u popodnevnim terminima  
✅ Minimizira se broj dana s prekomjernim opterećenjem

---

## 🧾Implementirane funkcionalnosti
 - Zakazivanje predavanja i vježbi za svih 5 godina
- Poštivanje preferenci i dostupnosti profesora
- Poseban tretman izbornih kolegija (zajednički termini)
- Razlikovanje laboratorijskih učionica od običnih
- Automatski izvoz u .html, .csv, i .xlsx formate
- Terminalski prikaz za brzi pregled rasporeda
---
## 🗂️ Struktura projekta
```
📁 Robotika_Projekt /
├── 📄 1_godina_timetable.html
├── 📄 1_godina_optimized_timetable.html
├── 📄 1_godina_timetable_matrix.csv
├── 📄 1_godina_optimized_timetable_matrix.csv
├── 📄 1_godina_timetable_matrix.xlsx
├── 📄 1_godina_optimized_timetable_matrix.xlsx

├── 📄 2_godina_timetable.html
├── 📄 2_godina_optimized_timetable.html
├── 📄 2_godina_timetable_matrix.csv
├── 📄 2_godina_optimized_timetable_matrix.csv
├── 📄 2_godina_timetable_matrix.xlsx
├── 📄 2_godina_optimized_timetable_matrix.xlsx

├── 📄 3_godina_timetable.html
├── 📄 3_godina_optimized_timetable.html
├── 📄 3_godina_timetable_matrix.csv
├── 📄 3_godina_optimized_timetable_matrix.csv
├── 📄 3_godina_timetable_matrix.xlsx
├── 📄 3_godina_optimized_timetable_matrix.xlsx

├── 📄 4_godina_timetable.html
├── 📄 4_godina_optimized_timetable.html
├── 📄 4_godina_timetable_matrix.csv
├── 📄 4_godina_optimized_timetable_matrix.csv
├── 📄 4_godina_timetable_matrix.xlsx
├── 📄 4_godina_optimized_timetable_matrix.xlsx

├── 📄 5_godina_timetable.html
├── 📄 5_godina_optimized_timetable.html
├── 📄 5_godina_timetable_matrix.csv
├── 📄 5_godina_optimized_timetable_matrix.csv
├── 📄 5_godina_timetable_matrix.xlsx
├── 📄 5_godina_optimized_timetable_matrix.xlsx

├── 🐍 classes.py
├── 🐍 data.py
├── 🐍 display.py
├── 🐍 elective_scheduler.py
├── 🐍 greedy_scheduler.py
├── 🐍 hill_climb_optimizer.py
├── 🐍 html_and_csv_export.py
├── 🐍 main.py

├── 📝 README.md
└── 🧾 requirements.txt
```

## 🗂️Arhitektura rješenja

### `main.py`
- Glavni program.
- Poziva sve ostale module u ispravnom redoslijedu:
  1. Zakazuje izborne kolegije.
  2. Pokreće greedy algoritam za svaku godinu.
  3. Optimizira raspored hill climb algoritmom.
  4. Generira HTML i Excel/CSV tablice.

---

### `greedy_scheduler.py`
- Greedy zakazivanje obaveznih predmeta.
- Poštuje dostupnost profesora, vrstu učionice i zauzetost termina.
- Osigurava da se termini izbornih kolegija ne koriste ponovno.

---

### `hill_climb_optimizer.py`
- Premješta vježbe iza predavanja, ako je moguće.
- Računa score na temelju više faktora:
  - raspored po danima,
  - vrijeme održavanja (jutro bolje od večeri),
  - kompatibilnost termina s profesorovim mogućnostima,
  - ispravni odnosi predavanja i vježbi.
- Izbjegava zauzete termine i preklapanja s izbornim kolegijima.

---

### `elective_scheduler.py`
- Zakazuje izborne kolegije prije svih ostalih aktivnosti.
- Pronalazi zajedničke slobodne termine za sve godine koje slušaju određeni kolegij.
- Prednost daje terminima koje profesor preferira.

---

### `html_and_csv_export.py`
- Generira:
  - HTML raspored po danima i učionicama s bojama po tipu nastave ili učionici,
  - CSV tablice za svaku godinu,
  - XLSX verzije za lakše pregledavanje u Excelu.
- Također omogućuje promjenu prikaza prema tipu nastave ili učionici.

---

### `classes.py`
- Definira osnovne entitete:
  - `Subject` – ime, vrsta, godina, izborni ili obavezni,
  - `Professor` – ime, dostupni termini, predmeti,
  - `Classroom` – ime, je li laboratorij, zauzeti termini.

---

### `data.py`
- Sadrži:
  - sveučilišne učionice,
  - sve predmete razvrstane po godinama (i izborne),
  - popis profesora s pripadajućim predmetima i dostupnim terminima,
  - inicijalne prazne rasporede po godinama.

---

### `display.py`
- Jednostavan konzolni prikaz rasporeda za debugiranje.

---

## 🔢 Ulazni / Izlazni podaci
### Ulazni podaci:
- Popis svih kolegija s godinom, tipom nastave (predavanje/vježbe) i izbornosti.
- Popis profesora, njihovih kolegija i slobodnih termina.
- Dostupne učionice, uključujući je li riječ o laboratoriju.

### Izlazni podaci:
Za svaku godinu:
- `X_godina_timetable.html`
- `X_godina_optimized_timetable.html`
- CSV i XLSX verzije
- Konzolni prikaz za brzi pregled

---
## 💻 Korištene tehnologije

Projekt je izrađen u programskom jeziku **Python 3**, koristeći sljedeće alate i biblioteke:

| Biblioteka         | Namjena                                       |
|--------------------|-----------------------------------------------|
| `openpyxl`         | generiranje Excel tablica rasporeda           |
| `csv`              | izvoz u CSV format                            |
| `html`             | generacija vizualnog HTML prikaza rasporeda   |
---
## ▶️ Pokretanje projekta

```bash
# 1. Kloniranje repozitorija
git clone https://github.com/rstarcic/Robotika_Projekt.git
cd Robotika_Projekt

# 2. Instalacija paketa
pip install -r requirements.txt

# 3. Pokretanje glavnog programa
python main.py
```
## 📚 Zaključak
Projekt demonstrira kako se heuristički algoritmi i lokalna optimizacija mogu koristiti za rješavanje problema automatskog rasporeda predavanja uz stvarna ograničenja.
Sustav omogućuje fleksibilno proširenje i može poslužiti kao temelj za integraciju u obrazovne informacijske sustave.