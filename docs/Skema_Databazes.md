
# Smart Estate – Skema e Databazës

## 1. Databaza

Projekti Smart Estate përdor PostgreSQL.

Emri i databazës: smart_estate

Databaza është lidhur me aplikacionin Django dhe
tabelat janë krijuar përmes migrimeve.

## 2. Tabelat kryesore

### Perdorues
Tabela agjencia_perdorues ruan të dhënat e
administratorëve dhe agjentëve.

Fushat kryesore:
- id (Primary Key)
- username
- password
- emri
- roli

### Prona
Tabela agjencia_prona ruan pronat e agjencisë.

Fushat:
- id (Primary Key)
- agjent_id (Foreign Key)
- lloji
- qyteti
- cmimi
- siperfaqja

### Klienti
Tabela agjencia_klienti ruan klientët.

Fushat:
- id (Primary Key)
- emri
- kontakti

### Kerkesa
Tabela agjencia_kerkesa lidh klientët me pronat.

Fushat:
- id (Primary Key)
- prona_id (Foreign Key)
- klienti_id (Foreign Key)

### Vizita
Tabela agjencia_vizita ruan vizitat e klientëve.

Fushat:
- id (Primary Key)
- prona_id (Foreign Key)
- klienti_id (Foreign Key)
- data_vizites

## 3. Relacionet

- Një agjent mund të ketë shumë prona.
- Një pronë mund të ketë shumë kërkesa.
- Një klient mund të ketë shumë kërkesa.
- Një pronë mund të ketë shumë vizita.
- Një klient mund të ketë shumë vizita.

Lidhjet janë realizuar me ForeignKey.

## 4. Kufizimet

- Çdo tabelë ka një Primary Key.
- ForeignKey ruan lidhjet ndërmjet tabelave.
- Fushat e detyrueshme nuk pranohen bosh.
- Çmimi dhe sipërfaqja validohen në API
  që të jenë më të mëdha se zero.
- Për lidhjet kryesore është përdorur PROTECT,
  për të penguar fshirjen e të dhënave që
  përdoren nga regjistrime të tjera.

## 5. Ndryshimet nga dizajni fillestar

Struktura kryesore me pesë entitete është ruajtur
nga Raporti Teknik 1.

Te modeli Vizita është shtuar fusha
data_vizites për të ruajtur datën dhe orën
e vizitës.

Modeli Perdorues është implementuar duke
trashëguar AbstractUser të Django, i cili
ofron fusha dhe funksione të gatshme për
autentikimin e përdoruesve.

## 6. Kontrollimi

Tabelat janë kontrolluar në pgAdmin 4.

Janë testuar krijimi dhe leximi i të dhënave,
si dhe lidhjet ndërmjet pronave, klientëve,
kërkesave dhe vizitave.
