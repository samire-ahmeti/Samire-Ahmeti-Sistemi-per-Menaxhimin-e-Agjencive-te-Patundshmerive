# Smart Estate – Sistemi për Menaxhimin e Agjencive të Patundshmërive

**Studentja:** Samire Ahmeti
**Universiteti:** Universiteti “Ukshin Hoti” – Prizren
**Lënda:** Projekt – Praktikë Profesionale
**Viti akademik:** 2026/2027

## 1. Përshkrimi i projektit

Smart Estate është një aplikacion web për menaxhimin e agjencive të patundshmërive.

Qëllimi i këtij projekti është të lehtësojë regjistrimin, prezantimin dhe menaxhimin e pronave, klientëve, kërkesave dhe vizitave në një sistem të vetëm.

Aplikacioni ofron një faqe publike ku vizitorët mund të shfletojnë prona, si dhe një panel menaxhimi për administratorët dhe agjentët.

Projekti po zhvillohet gradualisht, sipas kërkesave të lëndës Projekt – Praktikë Profesionale.

## 2. Teknologjitë e përdorura

- **Python dhe Django** – zhvillimi i backend-it dhe logjikës së aplikacionit.
- **Django REST Framework** – krijimi i REST API-së.
- **PostgreSQL** – ruajtja dhe organizimi i të dhënave.
- **HTML, CSS dhe JavaScript** – ndërtimi i ndërfaqes së përdoruesit.
- **Git dhe GitHub** – ruajtja dhe ndjekja e progresit.
- **Visual Studio Code** – mjedisi i zhvillimit.

## 3. Funksionalitetet e realizuara

### Faqet publike

- Kryefaqja e Smart Estate.
- Lista e pronave me fotografi dhe informacione.
- Kërkimi dhe filtrimi i pronave sipas qytetit dhe llojit.
- Shfaqja e detajeve dhe fotografive të një prone.
- Faqja Rreth nesh.
- Faqja Shërbimet.
- Faqja Kontakt me formular funksional.

Mesazhet e dërguara nga formulari i kontaktit ruhen në PostgreSQL dhe mund të shihen nga administratori në Django Admin.

### Paneli i menaxhimit

- Hyrja dhe dalja nga sistemi.
- Role të përdoruesve: administrator dhe agjent.
- Panel me statistika për pronat, klientët dhe vizitat.
- Regjistrimi i pronave të reja.
- Ndryshimi dhe fshirja e pronave.
- Menaxhimi i klientëve: shtim, listim, kërkim, ndryshim dhe fshirje.
- Validimi i formularëve.
- Kontrolli i qasjes sipas rolit të përdoruesit.

### Backend dhe API

- Modelet dhe relacionet në PostgreSQL.
- REST API për pronat, klientët, kërkesat dhe vizitat.
- Operacione CRUD për modulet kryesore përmes API-së.
- Autentikim dhe kontroll bazik i lejeve.
- Validime të të dhënave përpara ruajtjes.

## 4. Struktura e projektit

Projekti është organizuar në këtë mënyrë:

- `config/` – konfigurimi kryesor i Django-s dhe URL-të.
- `agjencia/models.py` – modelet e databazës.
- `agjencia/views.py` – funksionet kryesore dhe API-ja.
- `agjencia/forms.py` – formulari për pronat.
- `agjencia/klienti_actions.py` – funksionet e menaxhimit të klientëve.
- `agjencia/prona_actions.py` – ndryshimi dhe fshirja e pronave.
- `agjencia/contact_views.py` – përpunimi i mesazheve të kontaktit.
- `agjencia/templates/agjencia/` – faqet HTML.
- `agjencia/static/agjencia/` – CSS, JavaScript dhe fotografitë e dizajnit.
- `agjencia/migrations/` – migrimet e databazës.
- `docs/` – dokumentacioni teknik.
- `manage.py` – komandat e Django-s.
- `requirements.txt` – bibliotekat e nevojshme.

Frontend-i është ndërtuar me Django Templates dhe është i integruar drejtpërdrejt me backend-in.

## 5. Databaza

Projekti përdor PostgreSQL me databazën `smart_estate`.

Modelet kryesore janë:

1. Perdorues
2. Prona
3. FotoProne
4. Klienti
5. Kerkesa
6. Vizita
7. MesazhKontakti

Relacionet realizohen përmes `ForeignKey`. Për shembull, një pronë lidhet me agjentin që e menaxhon, ndërsa kërkesat dhe vizitat lidhin klientët me pronat.

## 6. Instalimi dhe ekzekutimi

Për ta ekzekutuar projektin në kompjuter, nevojiten Python dhe PostgreSQL.

### Hapi 1 – Shkarkimi i projektit

```powershell
git clone https://github.com/samire-ahmeti/Samire-Ahmeti-Sistemi-per-Menaxhimin-e-Agjencive-te-Patundshmerive.git
```

Hapni dosjen e projektit në Visual Studio Code.

### Hapi 2 – Krijimi i mjedisit virtual

```powershell
python -m venv .venv
```

Aktivizimi në PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Hapi 3 – Instalimi i bibliotekave

```powershell
python -m pip install -r requirements.txt
```

### Hapi 4 – Konfigurimi i PostgreSQL

Krijoni një databazë me emrin `smart_estate`.

Në dosjen kryesore të projektit krijoni skedarin `.env` me konfigurimin:

```env
DB_NAME=smart_estate
DB_USER=postgres
DB_PASSWORD=vendos_fjalekalimin_tend
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=vendos_nje_celes_sekret_te_sigurt
```

Vlerat duhet të përshtaten me konfigurimin lokal. Skedari `.env` nuk duhet të ngarkohet në GitHub.

### Hapi 5 – Migrimet e databazës

```powershell
python manage.py migrate
```

### Hapi 6 – Krijimi i administratorit

```powershell
python manage.py createsuperuser
```

### Hapi 7 – Nisja e serverit

```powershell
python manage.py runserver
```

Aplikacioni hapet në:

`http://127.0.0.1:8000/`

## 7. Faqet kryesore të aplikacionit

| Faqja | Adresa |
|---|---|
| Kryefaqja | `/` |
| Pronat | `/pronat/` |
| Rreth nesh | `/rreth-nesh/` |
| Shërbimet | `/sherbimet/` |
| Kontakt | `/kontakt/` |
| Hyrja | `/hyrja/` |
| Paneli | `/paneli/` |
| Klientët | `/klientet/` |
| Shto pronë | `/shto-prone/` |
| Shto klient | `/shto-klient/` |
| Django Admin | `/admin/` |
| REST API | `/api/` |

Faqet e menaxhimit kërkojnë autentikim dhe lejet përkatëse.

## 8. Endpoint-et kryesore të API-së

| Endpoint | Përshkrimi |
|---|---|
| `/api/pronat/` | Menaxhimi i pronave |
| `/api/klientet/` | Menaxhimi i klientëve |
| `/api/kerkesat/` | Menaxhimi i kërkesave |
| `/api/vizitat/` | Menaxhimi i vizitave |

API-ja është krijuar me Django REST Framework. Qasja në endpoint-e dhe veprimet e lejuara varen nga autentikimi dhe lejet e përdoruesit.

## 9. Shembull i integrimit frontend-backend

Një nga funksionalitetet kryesore është regjistrimi i një prone.

Rrjedha e funksionimit:

1. Përdoruesi hyn në panel.
2. Klikon butonin Shto pronë.
3. Plotëson formularin me të dhënat e pronës.
4. Django kontrollon vlefshmërinë e të dhënave.
5. Prona ruhet në PostgreSQL.
6. Përdoruesi ridrejtohet te detajet e pronës.
7. Prona e regjistruar shfaqet edhe në listën e pronave.

Ky funksionalitet demonstron lidhjen e ndërfaqes me backend-in dhe databazën.

## 10. Testimi i funksionaliteteve

Gjatë zhvillimit janë kryer kontrolle praktike për:

- Hyrjen dhe daljen nga sistemi.
- Regjistrimin dhe ndryshimin e pronave.
- Fshirjen e pronave testuese.
- Regjistrimin, ndryshimin dhe fshirjen e klientëve.
- Dërgimin dhe ruajtjen e mesazheve të kontaktit.
- Validimin e të dhënave në formularë.
- Shfaqjen e të dhënave të ruajtura në panel.

Testimi më i plotë, kontrollet shtesë të sigurisë dhe përgatitja për deployment do të vazhdojnë në fazat e ardhshme.

## 11. Gjendja aktuale e projektit

**Raporti Teknik 1:** Analiza, kërkesat dhe dizajni fillestar.

**Raporti Teknik 2:** Implementimi i databazës, backend-it dhe API-së.

**Raporti Teknik 3:** Frontend-i dhe integrimi funksional. Janë realizuar faqet publike, paneli i menaxhimit, moduli i pronave, moduli i klientëve dhe kontakti funksional.

Puna që vazhdon në këtë fazë:

- Ndërfaqja për menaxhimin e kërkesave.
- Ndërfaqja për menaxhimin e vizitave.
- Kontrollet përfundimtare të integrimit.
- Dokumentimi dhe demonstrimi i funksionaliteteve.

**Raporti Teknik 4:** Testimi më i plotë, siguria dhe përgatitja e versionit beta.

Projekti aktualisht ekzekutohet në mjedis lokal.

## 12. Repository dhe dokumentimi

Kodi burimor dhe historia e zhvillimit gjenden në GitHub:

[Smart Estate – GitHub Repository](https://github.com/samire-ahmeti/Samire-Ahmeti-Sistemi-per-Menaxhimin-e-Agjencive-te-Patundshmerive)

Dokumentacioni teknik i projektit ruhet në dosjen `docs/`.

Projekti është duke u zhvilluar për lëndën **Projekt – Praktikë Profesionale**, viti akademik **2026/2027**.