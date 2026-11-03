
# Smart Estate – Sistemi për Menaxhimin e Agjencive të Patundshmërive

**Studentja:** Samire Ahmeti
**Lënda:** Projekt – Praktikë Profesionale
**Universiteti:** Universiteti "Ukshin Hoti" – Prizren
**Viti akademik:** 2026/2027

## Përshkrimi i projektit

Smart Estate është një aplikacion për menaxhimin e agjencive të patundshmërive.

Qëllimi i projektit është organizimi i të dhënave për pronat, klientët, kërkesat dhe vizitat në një sistem të vetëm.

Projekti zhvillohet me Python dhe Django, ndërsa të dhënat ruhen në PostgreSQL.

## Teknologjitë

- Python
- Django
- Django REST Framework
- PostgreSQL
- Git dhe GitHub
- Visual Studio Code

## Funksionalitetet e implementuara

- Menaxhimi i përdoruesve dhe roleve bazike.
- Regjistrimi dhe menaxhimi i pronave.
- Regjistrimi dhe menaxhimi i klientëve.
- Menaxhimi i kërkesave për prona.
- Regjistrimi i vizitave.
- API CRUD për modulet kryesore.
- Autentikimi dhe autorizimi bazik.
- Validimi i çmimit dhe sipërfaqes së pronave.

## Instalimi dhe ekzekutimi

### 1. Shkarkimi i projektit

Shkarkoni repository-n nga GitHub dhe hapeni në Visual Studio Code.

### 2. Krijimi i mjedisit virtual

```powershell
python -m venv .venv
```

Aktivizimi në PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalimi i bibliotekave

```powershell
python -m pip install -r requirements.txt
```

### 4. Konfigurimi i PostgreSQL

Instaloni PostgreSQL dhe krijoni një databazë me emrin:

`smart_estate`

Në folderin kryesor të projektit krijoni skedarin `.env` dhe vendosni konfigurimet:

```env
DB_NAME=smart_estate
DB_USER=postgres
DB_PASSWORD=vendos_fjalekalimin_lokal
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=vendos_celesin_sekret_te_django
```

Vlerat e fjalëkalimit dhe çelësit sekret duhet të zëvendësohen me vlerat personale.

Skedari `.env` nuk duhet të publikohet në GitHub.

### 5. Krijimi i tabelave

```powershell
python manage.py migrate
```

### 6. Krijimi i administratorit

```powershell
python manage.py createsuperuser
```

### 7. Nisja e serverit

```powershell
python manage.py runserver
```

Pas nisjes, hapni:

- Django Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/

## Endpoint-et kryesore

| Metoda | Endpoint | Funksioni |
|---|---|---|
| GET, POST | /api/pronat/ | Leximi dhe krijimi i pronave |
| GET, PUT, PATCH, DELETE | /api/pronat/{id}/ | Menaxhimi i një prone |
| GET, POST | /api/klientet/ | Leximi dhe krijimi i klientëve |
| GET, PUT, PATCH, DELETE | /api/klientet/{id}/ | Menaxhimi i një klienti |
| GET, POST | /api/kerkesat/ | Leximi dhe krijimi i kërkesave |
| GET, POST | /api/vizitat/ | Leximi dhe krijimi i vizitave |

API përdor autentikim dhe kontroll të lejeve për veprimet kryesore.

## Databaza

Databaza përmban pesë modele kryesore:

1. Perdorues
2. Prona
3. Klienti
4. Kerkesa
5. Vizita

Relacionet ndërmjet modeleve janë realizuar me ForeignKey.

## Dokumentimi

Në folderin `docs` gjenden:

- Raportet Teknike 1 dhe 2 në Word.
- Dokumentimi i API-së.
- Skema e databazës.
- Problemet teknike dhe zgjidhjet.

## Gjendja e projektit

Aktualisht është realizuar pjesa kryesore e databazës, backend-it dhe API-së.

Frontend-i i plotë dhe integrimi i tij janë planifikuar për fazat e ardhshme të projektit.

Aplikacioni aktualisht ekzekutohet në ambient lokal.
