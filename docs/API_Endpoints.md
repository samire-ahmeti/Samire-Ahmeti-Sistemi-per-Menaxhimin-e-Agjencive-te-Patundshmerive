
# Smart Estate – Dokumentimi i API-së

## Teknologjitë
- Python / Django
- Django REST Framework
- PostgreSQL

## Endpoint-et kryesore

| Metoda | Endpoint | Funksioni |
|---|---|---|
| GET | /api/pronat/ | Leximi i pronave |
| POST | /api/pronat/ | Krijimi i pronës |
| GET | /api/pronat/{id}/ | Leximi i një prone |
| PATCH | /api/pronat/{id}/ | Përditësimi i pronës |
| DELETE | /api/pronat/{id}/ | Fshirja e pronës |
| GET | /api/klientet/ | Leximi i klientëve |
| POST | /api/klientet/ | Krijimi i klientit |
| PATCH | /api/klientet/{id}/ | Përditësimi i klientit |
| DELETE | /api/klientet/{id}/ | Fshirja e klientit |
| GET | /api/kerkesat/ | Leximi i kërkesave |
| POST | /api/kerkesat/ | Krijimi i kërkesës |
| DELETE | /api/kerkesat/{id}/ | Fshirja e kërkesës |
| GET | /api/vizitat/ | Leximi i vizitave |
| POST | /api/vizitat/ | Krijimi i vizitës |
| DELETE | /api/vizitat/{id}/ | Fshirja e vizitës |

## Autentikimi dhe autorizimi

API kërkon që përdoruesi të jetë i autentikuar.

Administratori ka qasje në modulet kryesore.

Agjentët kanë qasje të kufizuar te pronat e tyre.

Për klientët, kërkesat dhe vizitat përdoren lejet e Django.

## Shembull kërkese POST

Endpoint: /api/klientet/

{
    "emri": "Elira Berisha",
    "kontakti": "044555666"
}

Rezultati i pritur: HTTP 201 Created

## Status codes

- 200 OK – Kërkesa u realizua me sukses.
- 201 Created – Të dhënat u krijuan.
- 204 No Content – Të dhënat u fshinë.
- 400 Bad Request – Të dhënat janë të pavlefshme.
- 403 Forbidden – Përdoruesi nuk ka leje.
- 404 Not Found – Objekti nuk ekziston ose nuk është i qasshëm.

## Testimet

Janë testuar operacionet CRUD për pronat dhe klientët.

Për kërkesat dhe vizitat janë testuar metodat GET, POST dhe DELETE.

Janë testuar gjithashtu:
- Refuzimi i çmimit negativ.
- Refuzimi i krijimit të klientit pa emër.
- Refuzimi i qasjes pa leje.
- Kufizimi i pronave sipas agjentit.
