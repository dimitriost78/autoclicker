# autoclicker
python autoclicker

# AutoClickerApp

AutoClickerApp è un'applicazione Python per la registrazione e la riproduzione di azioni del mouse e della tastiera. Permette di registrare i clic e gli input della tastiera, salvarli in un file JSON e riprodurre le azioni registrate. L'app è pensata per eseguire automaticamente sequenze di azioni in modo ripetuto.

## Funzionalità

- **Registrazione dei Clic**: Registra i clic del mouse e le digitazioni della tastiera, insieme a eventuali ritardi.
- **Riproduzione delle Azioni Registrate**: Esegue i clic e gli scorrimenti registrati, con supporto per i loop.
- **Interfaccia Grafica**: Facile da usare, con pulsanti per avviare/fermare la registrazione e riprodurre le azioni.
- **Salvataggio in JSON**: Salva le sequenze di clic e input in formato JSON per poterle riutilizzare successivamente.

## Prerequisiti

Assicurati di avere Python 3.6 o superiore installato. Inoltre, il progetto utilizza le seguenti librerie:

- `tkinter` (incluso in Python per creare GUI)
- `pynput` (per ascoltare e simulare eventi del mouse e della tastiera)
- `pyautogui` (per simulare i clic del mouse e digitazioni)

Per installare le dipendenze aggiuntive, puoi usare `pip`:

```bash
pip install pynput pyautogui
```
Esegui l'applicazione:

```bash
python autoClickerApp.py
```
## Utilizzo
- `Avvio della Registrazione`:

Premi Avvia Registrazione per iniziare a registrare clic e input della tastiera.
I numeri inseriti con la tastiera vengono salvati per ciascun clic.

- `Interruzione della Registrazione`:

Premi Esc per fermare la registrazione.
Le azioni vengono salvate in un file JSON nella cartella specificata.

- `Riproduzione delle Azioni`:

Premi Riproduci per eseguire la sequenza di azioni registrate.
Nei log, "0" viene visualizzato per i campi vuoti durante la riproduzione senza modificare i dati originali nel JSON.

- `Chiusura dell'Applicazione`:

Usa il pulsante Esci per chiudere l'applicazione.

## Licenza
Questo progetto è distribuito sotto la licenza MIT. Vedi il file LICENSE per maggiori dettagli.