from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Asset, PriceHistory
from app.services.api_client import CoinGeckoClient
"""
STEP 6: app/routes.py - Alla URL-routes för din app

Routes definierar vilka URL:er som existerar och vad som händer när
användaren besöker dem.

Vi använder Blueprints - det är som "moduler" som grupperar relaterade routes.
Vi har 3 blueprints:
1. main_bp - Hempage och allmänna sidor
2. auth_bp - Login, register, logout
3. dashboard_bp - Dashboard och kryptoinformation
"""


main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# ============================================================================
# STEP 2: Index route (HOME PAGE)
# ============================================================================
# Denna route:
# 1. Om user är redan inloggad (@current_user.is_authenticated = True)
#    → Skicka till dashboard (redirect)
# 2. Annars
#    → Visa index.html (render_template)
#
# Tips:
# - redirect(url_for('dashboard.dashboard')) - skicka till dashboard route
# - render_template('index.html') - visa index.html template


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')


@login_required
@dashboard_bp.route('/')
def dashboard():
    assets = current_user.watched_assets
    return render_template('dashboard.html', assets=assets)


@login_required
@dashboard_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()

        if not query:
            flash('Sökfältet får inte vara tomt.', 'warning')
            return redirect(url_for('dashboard.dashboard'))
        # Sök i databasen efter matchande krypton
        coins = CoinGeckoClient.get_cryptocurrency_list()
        results = [coin for coin in coins if query.lower(
        ) in coin['name'].lower() or query.lower() in coin['symbol'].lower()]
        if not results:
            flash('Inga krypton hittades som matchar din sökning.', 'info')
            return redirect(url_for('dashboard.dashboard'))
        return render_template('search_results.html', results=results, query=query)
    return redirect(url_for('dashboard.dashboard'))


@login_required
@dashboard_bp.route('/add_asset', methods=['POST'])
def add_asset():
    query = request.form.get('query', '').strip()
    if not query:
        flash('Sökfältet får inte vara tomt.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    price_data = CoinGeckoClient.get_current_price(query)
    if not price_data:
        flash('Kryptot hittades inte. Försök igen.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    asset = Asset.query.filter_by(coingecko_id=query).first()
    if not asset:
        asset = Asset(
            coingecko_id=query,
            name=request.form.get('name', 'Unknown'),
            symbol=request.form.get('symbol', 'N/A'),
            current_price=price_data.get('usd')
        )
        db.session.add(asset)
        current_user.watched_assets.append(asset)
        db.session.commit()
        flash(f'{asset.name} har lagts till i din dashboard!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    if asset in current_user.watched_assets:
        flash('Du har redan lagt till detta kryptot i din dashboard.', 'info')
        return redirect(url_for('dashboard.dashboard'))

    current_user.watched_assets.append(asset)
    db.session.commit()
    flash(f'{asset.name} har lagts till i din dashboard!', 'success')
    return redirect(url_for('dashboard.dashboard'))


"""
SÄKERHETSNOTE:
- @login_required skyddar routes så bara inloggade kan nå dem
- check_password_hash kontrollerar lösenord säkert (aldrig lagra plain text!)
- current_user är alltid tillgänglig - Flask-Login hanterar det
"""
