
# 1. Frontend Dokumentacija — Girls in Science Platform (Tim 3)

## 1. Pregled aplikacije
Girls in Science Platform frontend je Vue 3 aplikacija koja korisnicama omogućava pregled i interakciju sa sadržajem platforme — direktorij inspirativnih žena iz STEM oblasti, blog objave i vijesti centra, radionice, mentorstvo i upravljanje profilom. Aplikacija komunicira sa FastAPI backendom putem REST API poziva.

## 2. Tehnologije

Framework: Vue 3 (Composition API)
Build tool: Vite
CSS framework: Tailwind CSS
Routing: Vue Router 4
HTTP komunikacija: Fetch API (centralizovano u api.js)
UI biblioteke: SweetAlert2, @vueform/multiselect

## 3. Struktura projekta

frontend/
├── src/
│   ├── components/
│   │   ├── NavBar.vue           # Navigacijski meni
│   │   └── NewsCard.vue         # Kartica za prikaz blog objave u listi
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── rolemodels/
│   │   │   ├── RoleModelsView.vue   # Lista profila uzora sa pretragom
│   │   │   ├── RoleModelDetail.vue  # Detalji profila
│   │   │   ├── RoleModelAdd.vue     # Forma za kreiranje profila
│   │   │   ├── RoleModelEdit.vue    # Forma za uređivanje profila
│   │   │   └── BookmarksView.vue    # Lista favorita korisnice
│   │   ├── news/
│   │   │   ├── NewsView.vue         # Lista blog objava sa filterom po kategoriji
│   │   │   ├── NewsDetail.vue       # Detalji blog objave
│   │   │   ├── CreateNewsView.vue   # Forma za kreiranje objave
│   │   │   └── NewsEdit.vue         # Forma za uređivanje objave
│   │   ├── workshops/
│   │   ├── mentoring/
│   │   ├── profiles/
│   │   └── admin/
│   ├── services/
│   │   └── api.js               # Centralizovani API pozivi
│   ├── router/
│   │   └── index.js             # Definicija ruta i navigation guards
│   └── main.js
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json

## 4. Pokretanje projekta

Instalacija zavisnosti
cd frontend
npm install

Pokretanje razvojnog servera
npm run dev

Aplikacija je dostupna na http://localhost:5173.
Konfiguracija
Frontend ne koristi .env fajl — base URL backenda je definisan direktno u src/services/api.js: const BASE_URL = 'http://127.0.0.1:8000'

## 5. Komunikacija sa backendom
Sva komunikacija sa backendom odvija se kroz centralizovani servisni sloj u fajlu src/services/api.js. Svaka funkcija u ovom fajlu odgovara jednom API endpointu i šalje HTTP zahtjev korištenjem Fetch API-ja.

Autentifikacija
Nakon uspješnog logina, JWT token se čuva u localStorage pod ključem token. Zaštićeni API pozivi token dohvataju interno unutar funkcije iz localStorage i šalju ga u Authorization: Bearer <token> headeru. Uloga korisnice (user_role) također se čuva u localStorage i koristi u navigation guardovima.
Navigation guards
U router/index.js definisana su dva meta polja:

requiresAuth: true — neprijavljena korisnica se preusmjerava na /login
requiresAdmin: true — korisnica bez admin uloge se preusmjerava na /unauthorized
guestOnly: true — prijavljena korisnica se preusmjerava na /

## 6. Član 1 - Čerkezović Dženan

Pregled implementiranih funkcionalnosti
RoleModelsView.vue — implementirao pretragu/filter u realnom vremenu po imenu, STEM oblasti i instituciji kroz computed property filteredRoleModels. Pretraga filtrira lokalno nad već dohvaćenom listom bez dodatnih API poziva. Reset dugme se pojavljuje samo kada je pretraga aktivna. Admin vidi dugme za dodavanje novog profila, prijavljene korisnice koje nisu admin vide dugme za odlazak na stranicu favorita.
RoleModelAdd.vue — kreirao stranicu za dodavanje novog profila. Implementirana frontend validacija svih obaveznih polja kroz validate() funkciju sa prikazom grešaka ispod svakog polja, upload profilne slike, poruka potvrde i automatsko preusmjeravanje nakon uspješnog kreiranja. Zaštita od višestrukog submita kombinacijom isLoading flaga i @click.once direktive.
RoleModelDetail.vue — implementirao pametnu navigaciju nazad kroz route.query.from i route.query.newsId parametre — dugme vraća korisnika tamo odakle je došao (lista profila, favoriti ili detalji blog objave). Implementirao SweetAlert2 modalni prozor za potvrdu brisanja profila umjesto nativnog confirm() dijaloga.
RoleModelEdit.vue — implementirao zaštitu od višestrukog submita, ispravnu logiku uklanjanja profilne slike i usklađenu validaciju sa Add formom.
BookmarksView.vue — implementirao ispravnu logiku uvjetnog prikaza profilne fotografije — prikazuje sliku ako postoji, inicijale kao fallback ako ne postoji, konzistentno sa ostalim komponentama koje prikazuju profile.
NewsDetail.vue — kreirao stranicu koja prikazuje detalje pojedinačne blog objave: naslov, datum, autora, naslovnu sliku, sadržaj, kategorije i listu povezanih profila uzora. Klik na povezani profil vodi na detalje tog profila sa query parametrima from: 'news' i newsId kako bi navigacija nazad bila ispravna. Implementirao SweetAlert2 za potvrdu brisanja objave.
CreateNewsView.vue — implementirao zaštitu od višestrukog submita, dodao v-model na textarea za sadržaj koji je nedostajao, uskladio Multiselect konfiguraciju sa NewsEdit.vue, dodao outer wrapper div za vizuelnu konzistentnost sa ostatkom projekta, implementirao upload naslovne slike i odabir kategorija.
NewsEdit.vue — kreirao stranicu za uređivanje blog objave. Pri učitavanju paralelno dohvata podatke objave i listu svih profila kroz Promise.all. Forma se automatski puni postojećim podacima. Implementirana validacija, zaštita od višestrukog submita i upload naslovne slike.

Putanja                 Komponenta              Auth
/role-models            RoleModelsView.vue       ne    
/role-models/add        RoleModelAdd.vue         da
/news/:id               NewsDetail.vue           ne
/news/create            CreateNewsView.vue       da
/news/:id/edit          NewsEdit.vue             da


API funkcije
addRoleModel(data, token) — POST /role-models/, sa Bearer tokenom
deleteRoleModel(id, token) — DELETE /role-models/{id}, sa Bearer tokenom
getNewsPost(id) — GET /news/{id}, bez autentifikacije
updateNewsPost(id, data) — PATCH /news/{id}, token iz localStorage
uploadNewsImage(formData) — POST /news/upload-image, multipart/form-data



## 7. Član 2 - Amina Sarhatlić

Pregled implementiranih funkcionalnosti
RoleModelDetail.vue — inicijalno kreirala stranicu koja prikazuje detalje profila uzora: ime, prezime, STEM oblast, instituciju, poziciju, biografiju i postignuća. Dodala prikaz poruke o grešci ako profil ne postoji. Dodala bookmark dugme vidljivo samo prijavljenim korisnicama koje nisu admin, te dugmad za uređivanje i brisanje vidljiva samo adminu. Povezala RoleModelCard.vue sa stranicom detalja.
RoleModelEdit.vue — inicijalno kreirala stranicu za uređivanje profila sa prefill formom koja se puni postojećim podacima pri učitavanju, validacijom obaveznih polja i porukom o uspjehu nakon ažuriranja.
NewsView.vue — kreirala stranicu koja prikazuje listu svih blog objava. Implementirala filter po kategorijama kroz dugmiće, abecedno sortiranje kategorija, prikaz poruke kada nema objava i formu za kreiranje kategorija vidljivu samo administratorici.
NewsCard.vue — kreirala reusable komponentu koja prikazuje karticu blog objave u listi: naslov, datum i kategorije kao tagove. Klik preusmjerava na stranicu detalja objave.
ConfirmDeleteModal.vue — kreirala modal komponentu za potvrdu brisanja. Prima message prop i emituje confirm i cancel evente prema roditeljskoj komponenti.
BookmarksView.vue — inicijalno kreirala stranicu koja prikazuje listu profila koje je korisnica sačuvala u favourite. Dostupna samo prijavljenim korisnicama.


Putanja                     Komponenta              Auth
/role-models/:id            RoleModelDetail.vue      ne
/role-models/:id/edit       RoleModelEdit.vue        da
/news                       NewsView.vue             ne
/bookmarks                  BookmarksView.vue        da


API funkcije
getRoleModel(id) — GET /role-models/{id}, bez autentifikacije
updateRoleModel(id, data) — PATCH /role-models/{id}, token iz localStorage
getNewsPosts() — GET /news/, bez autentifikacije
deleteNewsPost(id, token) — DELETE /news/{id}, sa Bearer tokenom
getCategories() — GET /news/categories, bez autentifikacije
createCategory(data, token) — POST /news/categories, sa Bearer tokenom
getBookmarks() — GET /bookmarks/, token iz localStorage
addBookmark(roleModelId) — POST /bookmarks/{id}, token iz localStorage
removeBookmark(roleModelId) — DELETE /bookmarks/{id}, token iz localStorage



## 8. Član 3 - Šejla Valjevac

Pregled implementiranih funkcionalnosti
RoleModelsView.vue — implementirala inicijalnu stranicu koja prikazuje listu svih profila uzora sa osnovnim informacijama (ime, prezime, STEM oblast, institucija). Izvršila redizajn stranice — modernizovan izgled kartica profila, poboljšan raspored elemenata i preglednost sadržaja.
RoleModelAdd.vue — učestvovala u razvoju forme za dodavanje novog profila. Izvršila redizajn forme — poboljšan izgled inputa i layout stranice, implementirana podrška za upload i prikaz profilne fotografije.
RoleModelEdit.vue — učestvovala u razvoju forme za uređivanje profila. Izvršila redizajn forme konzistentno sa Add formom, implementirana podrška za prikaz i promjenu profilne fotografije.
RoleModelDetail.vue — učestvovala u razvoju stranice detalja profila. Izvršila redizajn stranice — modernizovan prikaz biografije i postignuća, poboljšan vizualni layout.
CreateNewsView.vue — implementirala stranicu za kreiranje blog objave sa formom koja sadrži polja za naslov i sadržaj, validacijom unesenih podataka i mogućnošću odabira povezanih profila iz direktorija kroz multiselect komponentu. Izvršila redizajn forme, implementirala podršku za upload naslovne slike.
NewsView.vue — učestvovala u redizajnu početne stranice novosti.
NewsDetail.vue — učestvovala u razvoju i redizajnu stranice detalja objave, uključujući prikaz povezanih profila.
NewsEdit.vue — učestvovala u redizajnu forme za uređivanje objave.

Putanja                 Komponenta              Auth
/role-models            RoleModelsView.vue       ne
/news/create            CreateNewsView.vue       da

API funkcije 
getRoleModels() — GET /role-models/, bez autentifikacije
createNewsPost(data, token) — POST /news/, sa Bearer tokenom