# Mihir Raja — Flask Portfolio

**Run locally**
```bash
pip install -r requirements.txt
python app.py
```

**Deploy (Render/Heroku)**
- Uses `Procfile` with `web: gunicorn app:app`
- Set `SECRET_KEY` as an env var