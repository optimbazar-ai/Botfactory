from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.bot import Bot
from app.forms import BotForm

bot_bp = Blueprint('bot', __name__, url_prefix='/bots')


@bot_bp.route('/')
@login_required
def list_bots():
    """List all bots for the current user."""
    bots = Bot.query.filter_by(user_id=current_user.id).order_by(Bot.created_at.desc()).all()
    return render_template('bots/list.html', bots=bots)


@bot_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_bot():
    """Create a new bot."""
    # Check subscription limits
    if current_user.subscription_type == 'free':
        bot_count = Bot.query.filter_by(user_id=current_user.id).count()
        if bot_count >= 1:
            flash('You have reached the maximum number of bots for free plan (1 bot). Please upgrade your subscription to create more bots.', 'warning')
            return redirect(url_for('bot.list_bots'))
    
    form = BotForm()
    
    if form.validate_on_submit():
        bot = Bot(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            language=form.language.data,
            platform=form.platform.data,
            system_prompt=form.system_prompt.data,
            telegram_token_1=form.telegram_token_1.data
        )

        # If there's an old telegram_token field, migrate it
        if hasattr(form, 'telegram_token') and form.telegram_token.data:
            if not bot.telegram_token_1:
                bot.telegram_token_1 = form.telegram_token.data
        
        db.session.add(bot)
        db.session.commit()
        
        flash(f'Bot "{bot.name}" created successfully!', 'success')
        return redirect(url_for('bot.list_bots'))
    
    return render_template('bots/new.html', form=form)


@bot_bp.route('/<int:bot_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_bot(bot_id):
    """Edit an existing bot."""
    bot = Bot.query.filter_by(id=bot_id, user_id=current_user.id).first_or_404()
    
    form = BotForm(obj=bot)
    
    if form.validate_on_submit():
        # Update bot fields
        bot.name = form.name.data
        bot.description = form.description.data
        bot.language = form.language.data
        bot.platform = form.platform.data
        bot.system_prompt = form.system_prompt.data
        bot.telegram_token_1 = form.telegram_token_1.data
        bot.is_active = 'is_active' in request.form  # Handle checkbox
        
        db.session.commit()
        
        flash(f'Bot "{bot.name}" updated successfully!', 'success')
        return redirect(url_for('bot.list_bots'))
    
    return render_template('bots/edit.html', form=form, bot=bot)


@bot_bp.route('/<int:bot_id>/delete', methods=['POST'])
@login_required
def delete_bot(bot_id):
    """Delete a bot."""
    bot = Bot.query.filter_by(id=bot_id, user_id=current_user.id).first_or_404()
    
    bot_name = bot.name
    db.session.delete(bot)
    db.session.commit()
    
    flash(f'Bot "{bot_name}" deleted successfully!', 'info')
    return redirect(url_for('bot.list_bots'))
