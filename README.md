# Apskaitininkas

Sveiki atvykę į Apskaitininkas - Django pagrindu sukurtą projektą, skirtą sąskaitų ir finansinių operacijų valdymui.

## Reikalavimai

- Python 3.8 ar naujesnė versija
- Django 5.1.4
- Bootstrap 4.1.3 (front-end stilizacijai)
- SQLite (numatytoji duomenų bazė)

## Diegimas

1. **Klonuokite repozitoriją**:

   ```bash
   git clone <projekto-repozitorijos-nuoroda>
   cd <projekto-repozitorijos-aplankas>
   ```

2. **Sukurkite virtualią aplinką**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate   # Windows
   ```

3. **Įdiekite priklausomybes**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Paleiskite duomenų bazės migracijas**:

   ```bash
   python manage.py migrate
   ```

5. **Sukurkite administratoriaus vartotoją**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Paleiskite serverį**:

   ```bash
   python manage.py runserver
   ```

7. **Atidarykite projektą naršyklėje**:

   Eikite į [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Funkcionalumas

### Pagrindinės funkcijos:
- **Klientų valdymas**:
  - Pridėti, redaguoti ir ištrinti klientus.
- **Prekių valdymas**:
  - Pridėti, redaguoti ir tvarkyti prekių kategorijas.
- **Sąskaitų valdymas**:
  - Kurti, redaguoti ir peržiūrėti išrašytas bei gautas sąskaitas.
- **Finansinės operacijos**:
  - Automatinis operacijų generavimas pagal sąskaitų duomenis.

## Naudojimas

1. **Prisijungimas**:
   - Eikite į prisijungimo puslapį [http://127.0.0.1:8000/apskaitininkas/login/](http://127.0.0.1:8000/apskaitininkas/login/).
   - Prisijunkite naudodami savo vartotojo vardą ir slaptažodį.

2. **Navigacija**:
   - Viršutinėje naršymo juostoje pasirinkite norimą sekciją: Klientai, Prekės, Sąskaitos, Operacijos ar Statistika.

3. **Sąskaitų kūrimas**:
   - Eikite į "Invoices" ir pasirinkite "Create Invoice".
   - Užpildykite pagrindinę sąskaitos informaciją bei pridėkite sąskaitos eilutes.

4. **Statistikos peržiūra**:
   - Eikite į "Statistics", kad peržiūrėtumėte vizualizuotus pajamų ir išlaidų duomenis.

## Failų struktūra

- `models.py` - Duomenų bazės modeliai.
- `views.py` - Vaizdų funkcijos, atsakingos už puslapių logiką.
- `forms.py` - Django formos duomenų įvedimui ir validacijai.
- `urls.py` - URL nukreipimų konfigūracija.
- `templates/` - HTML šablonai (naudojama Bootstrap).
- `static/` - CSS ir JavaScript failai.

## Kontaktai

motiejus.dilys@gmail.com



