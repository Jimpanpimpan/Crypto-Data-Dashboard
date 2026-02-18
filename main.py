from app import create_app

"""
STEP 2: main.py - Entry point för din applikation

Denna fil är det första som körs när du startar appen.
Det enda den gör är att importera och starta Flask-appen.
"""
app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)


# TODO 1: Importera create_app från app/__init__.py
# Syntax: from app import create_app

# TODO 2: Skapa Flask-appen med development config
# Skapa en variabel 'app' som använder create_app('development')

# TODO 3: Skapa en if-sats: if __name__ == '__main__':
# Det här säger: "Om denna fil körs direkt (inte importerad från någon annan fil)"
#
# Inuti denna if-sats, starta servern med:
# app.run(debug=True, host='127.0.0.1', port=5000)
#
# Förklaringar:
# - debug=True: Servern startar om när du ändrar kod
# - host='127.0.0.1': Endast lokala anslutningar
# - port=5000: Besök http://localhost:5000 i din browser

"""
TIPS:
- __name__ är en built-in Python variabel
- Om du kör main.py direkt: __name__ = '__main__'
- Om du importerar main från annat: __name__ = 'main'
"""
