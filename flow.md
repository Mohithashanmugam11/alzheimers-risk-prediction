ALZHEIMER_APP/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── memory_game.html
│   ├── reaction_game.html
│   ├── result.html
│   └── signup.html
│
├── app.py                # Flask main app
├── setup_db.py           # Script to initialize database
├── users.db              # SQLite DB (⚠️ better keep this in .gitignore)
├── stacked_model.pkl     # Trained ML model
├── column_order.pkl      # Preprocessing artifact
├── label_encoder.pkl     # Encoder artifact
├── requirements.txt      # Dependencies (you create this)
├── README.md             # Project overview
├── .gitignore            # Ignore unnecessary files
