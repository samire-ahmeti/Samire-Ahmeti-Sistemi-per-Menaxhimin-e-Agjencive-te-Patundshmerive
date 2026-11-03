
# Smart Estate – Problemet Teknike dhe Zgjidhjet

## 1. Problemi me lidhjen e PostgreSQL

Gjatë konfigurimit të databazës, fillimisht
kishim vështirësi me lidhjen ndërmjet Django
dhe PostgreSQL.

Problemi lidhej me emrin e databazës,
i cili kishte një hapësirë shtesë.

Zgjidhja:
E korrigjuam emrin në smart_estate dhe
kontrolluam konfigurimin në skedarin .env.

Pas kësaj, lidhja me PostgreSQL funksionoi.

## 2. Problemi me hyrjen e agjentit

Gjatë testimit të autentikimit, përdoruesi
agjent1 nuk mund të hynte me fjalëkalimin
e vendosur fillimisht.

Zgjidhja:
Përdorëm komandën e Django:

python manage.py changepassword agjent1

Pas ndryshimit të fjalëkalimit, agjenti
u autentikua me sukses.

## 3. Problemi me importimin e ViewSet

Gjatë zhvillimit të API-së, Django shfaqi
gabimin:

ImportError: cannot import name 'VizitaViewSet'

Zgjidhja:
Kontrolluam agjencia/views.py dhe
rikthyem klasën VizitaViewSet.

Pastaj ekzekutuam:

python manage.py check

Kontrolli përfundoi pa gabime.

## 4. Problemi me testimin e API-së

Gjatë testimit me APIClient në Django Shell,
morëm gabimin:

Invalid HTTP_HOST header: 'testserver'

Zgjidhja:
Përdorëm override_settings me ALLOWED_HOSTS
vetëm gjatë testimit, pa ndryshuar
konfigurimin e projektit.

Pas kësaj, testuam autorizimin dhe API
ktheu HTTP 403 Forbidden për përdoruesin
që nuk kishte leje.

## 5. Kontrollimi i autorizimit

Fillimisht, API përdorte vetëm
IsAuthenticated dhe nuk kufizonte
mjaftueshëm qasjen sipas lejeve.

Zgjidhja:
Shtuam kufizimin e pronave sipas agjentit
dhe kontrollin e lejeve për modulet e tjera.

Testuam që agjent1 nuk mund ta lexonte
pronën e agjent2 dhe nuk kishte leje për
të krijuar klientë.
