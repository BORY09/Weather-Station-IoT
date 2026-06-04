# Weather-Station-IoT: Rozproszony, Wielowęzłowy System Monitorowania Parametrów Środowiskowych

### 📝 Opis Projektu
Kompleksowy system klasy End-to-End zaprojektowany i wykonany w ramach pracy inżynierskiej na kierunku Informatyka. System realizuje asynchroniczną akwizycję, bezprzewodową transmisję oraz wizualizację w czasie rzeczywistym parametrów atmosferycznych oraz wskaźników jakości powietrza (CO2, LZO, ciśnienie, temperatura, wilgotność).

Projekt opiera się na skalowalnej architekturze **Publish/Subscribe (IoT)**, eliminującej tradycyjne odpytywanie bazy danych (polling) na rzecz natychmiastowego dostarczania zdarzeń (push) do warstwy prezentacji.

---

### 🏗️ Architektura Systemu i Moduły

System składa się z trzech niezależnych warstw technologicznych współpracujących w sieci lokalnej:

1. **Węzeł Pomiarowy (Edge Device):** 
   Oprogramowanie układowe napisane w języku **MicroPython** dla mikrokontrolera **Adafruit ESP32 Huzzah** (stacja bazowa Grove). Odpowiada za:
   - Integrację czujników cyfrowych (DHT22, CCS811, MPL3115A2) za pośrednictwem magistrali **I2C**.
   - Lokalny, bezpieczny zapis danych pomiarowych na kartę **MicroSD** przez magistralę **SPI** (Logger 3.3V).
   - Lokalny podgląd danych na miniaturowym ekranie **OLED SSD1306**.
   - Publikowanie (Publish) spakietowanych danych strukturalnych do brokera sieciowego przez Wi-Fi.

2. **Centrum Komunikacyjne i Logika Serwerowa:**
   Serce sieciowe systemu uruchomione na minikomputerze **Raspberry Pi 4** (system operacyjny **Raspbian**):
   - **Broker MQTT 3.1 Mosquitto:** Odpowiada za centralne zarządzanie ruchem sieciowym, subskrypcjami i asynchronicznym przekazywaniem komunikatów.
   - **Skrypty Systemowe (Python):** Daemony uruchamiane w tle, odpowiedzialne za dodatkową walidację danych oraz automatyzację zadań sieciowych.

3. **Węzeł Odbiorczy (Hardware Client):**
   Dedykowana, fizyczna stacja odbiorcza oparta na drugim mikrokontrolerze **ESP32**, która subskrybuje tematy MQTT i w czasie rzeczywistym prezentuje kluczowe odczyty na alfanumerycznym wyświetlaczu **LCD 16x2**.

4. **Dashboard Analityczny (Frontend WWW):**
   Autorski, responsywny interfejs webowy **(HTML5, CSS3, JavaScript ES6+)** umożliwiający zdalny monitoring bez opóźnień:
   - Zastosowanie biblioteki **Eclipse Paho MQTT (mqttws31.js)** do nawiązywania bezpośrednich połączeń **WebSockets** z brokerem z poziomu przeglądarki.
   - Wykorzystanie profesjonalnego silnika **Highcharts** do renderowania płynnych, dynamicznych wykresów trendów pogodowych w czasie rzeczywistym.

---

### 🛠️ Technologie i Narzędzia

* **Języki programowania:** Python (skrypty serwerowe), MicroPython (firmware urządzeń), JavaScript (asynchroniczny frontend), HTML5, CSS3.
* **Protokoły i Magistrale:** MQTT 3.1, WebSockets, I2C (z użyciem HUB I2C), SPI.
* **Środowiska programistyczne:** Thonny IDE (MicroPython), Raspberry Pi Ecosystem.
* **Wykorzystany Hardware:** Raspberry Pi 4, Adafruit ESP32 Huzzah, Grove Base Shield, czujniki DHT22, CCS811, MPL3115A2, ekrany OLED SSD1306 oraz LCD 16x2.
