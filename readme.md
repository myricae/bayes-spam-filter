# Naive Bayes SMS Classifier (Flask)

Applicazione web in Flask che addestra **Naive Bayes** su un sottoinsieme del dataset **SMS Spam Collection** e classifica un messaggio di testo come `ham` (legittimo) oppure `spam`. L’interfaccia è minimale: invii un testo, carichi (opzionale) un file di dati in formato `SMSSpamCollection`, e ottieni il responso con una stima di accuratezza.

> **Percorso file principali**:  
> - Backend: `first.py` (Flask)  
> - Template: `templates/classifier.html`, `templates/result.html`  
> - Statici/CSS: `static/css/*`  
> - Dataset di esempio: `datasets/smsspamcollection/SMSSpamCollection` (duplicato anche in `uploads/`)  

---

## Come funziona (in breve)
1. La route `GET /classifier` mostra un form per inserire il messaggio (`name="msg"`) e, se vuoi, caricare un file dataset (`name="browse"`).  
2. Alla `POST /classifier` il codice:  
   - legge il file in stile **SMS Spam Collection** (righe `label<TAB>testo`),  
   - tokenizza con **TextBlob**, rimuove stopword inglesi (libreria `stop-words`),  
   - costruisce una lista di tuple `(token, etichetta)` e fa uno *split* veloce (train/test),  
   - addestra **`textblob.classifiers.NaiveBayesClassifier`**,  
   - calcola `accuracy` sul piccolo test set,  
   - classifica il messaggio inviato e mostra il risultato in `result.html`.
3. Di default l’app parte su `0.0.0.0:8080` (vedi fondo di `first.py`).

> **Nota**: nel codice c’è un vecchio `UPLOAD_FOLDER = 'C:/Users/saverio/...'` pensato per Windows. Se necessario, cambialo in un percorso locale valido (es. `uploads/`).

---

## Requisiti
- **Python 3.9+** (funziona anche con 3.10/3.11; il codice contiene un `print` in stile Python 2, ma Flask gira regolarmente su Py3 sostituendo quelle stampe con `print()` nel caso serva).
- Librerie Python:
  - `flask`
  - `textblob`
  - `stop-words`
  - `jinja2` (già inclusa con Flask)
  - `requests` (opzionale, presente in `first.py`)
  - `werkzeug` (incluso con Flask)

Installazione rapida delle dipendenze:

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install flask textblob stop-words requests
python -m textblob.download_corpora # corpora minimi per TextBlob
