from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Asset, PriceHistory
from app.services.api_client import CoinGeckoClient

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')


@login_required
@dashboard_bp.route('/')
def dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Asset.query.join(Asset.followers)\
        .filter(User.id == current_user.id)\
        .paginate(page=page, per_page=per_page, error_out=False)

    assets = pagination.items

    return render_template('dashboard.html', assets=assets, pagination=pagination)


@login_required
@dashboard_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
    else:
        query = request.args.get('query', '').strip()

    if not query:
        flash('Sökfältet får inte vara tomt.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    coins = CoinGeckoClient.get_cryptocurrency_list()

    if not coins:
        flash('Kunde inte hämta kryptolistan. Försök igen senare.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    results = [coin for coin in coins if query.lower(
    ) in coin['name'].lower() or query.lower() in coin['symbol'].lower()]

    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]
    total_pages = (len(results) + per_page - 1) // per_page

    if not results:
        flash('Inga krypton hittades som matchar din sökning.', 'info')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('search_results.html',
                           results=paginated_results,
                           query=query,
                           page=page,
                           total_pages=total_pages,
                           total=len(results))


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


@login_required
@dashboard_bp.route('/remove_asset/<int:asset_id>', methods=['POST'])
def remove_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    if asset not in current_user.watched_assets:
        flash('Detta kryptot finns inte i din dashboard.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    current_user.watched_assets.remove(asset)
    db.session.commit()
    flash(f'{asset.name} har tagits bort från din dashboard.', 'success')
    return redirect(url_for('dashboard.dashboard'))
