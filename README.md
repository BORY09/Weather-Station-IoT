# Weather-Station-IoT: System Akwizycji i Analizy Danych Meteorologicznych
###  Opis Projektu

Kompleksowy system typu End-to-End zrealizowany w ramach pracy inżynierskiej na kierunku Informatyka.
Projekt obejmuje budowę fizycznych jednostek pomiarowych, bezprzewodową transmisję danych oraz ich składowanie i wizualizację w czasie rzeczywistym

Projekt składa się z trzech współpracujących modułów:
. **stacjanadawcza (Edge Devices):** Oprogramowanie mikrokontrolerów odpowiedzialne za odczyt parametrów z czujników atmosferycznych i ich pakietowanie do wysyłki.
2. **stacjaodbiorcza (Data Processing & ETL):** Serce systemu napisane w języku **Python**. Odpowiada za:
   - Odbiór danych surowych (Serial/Radio).
   - **Walidację danych** (filtracja błędów pomiarowych).
   - Zapis ustrukturyzowanych danych do bazy danych.
3. **stronaWWW (Data Visualization):** Dashboard analityczny oparty na **JavaScript (Chart.js)**, prezentujący trendy pogodowe, minima, maksima i bieżące odczyty.

### 🛠️ Technologie i Narzędzia
* **Języki:** Python 3.x, JavaScript (ES6+), HTML5, CSS3.
* **Analiza danych:** Pandas (opcjonalnie), Logika walidacji w czystym Pythonie.
* **Hardware:** Mikrokontrolery wspierane przez środowisko Thonny (MicroPython/Python).
* **Wizualizacja:** Chart.js, CSS Flexbox/Grid.
