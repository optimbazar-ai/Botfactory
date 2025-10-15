"""
Bot boshqaruvi - ishga tushirish/to'xtatish
"""
from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.bot import BotModel
from app.services.polling_service import polling_manager

bot_control_bp = Blueprint('bot_control', __name__)

@bot_control_bp.route('/bot/<int:bot_id>/start', methods=['POST'])
@login_required
def start_bot(bot_id):
    """Botni ishga tushirish"""
    bot = BotModel.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('Bu bot sizga tegishli emas!', 'error')
        return redirect(url_for('bot.list_bots'))
    
    # Check if already running
    if polling_manager.is_bot_running(bot_id):
        flash('Bot allaqachon ishlamoqda!', 'info')
        return redirect(url_for('bot.list_bots'))
    
    # Start bot
    result = polling_manager.start_bot(bot)
    
    if result['success']:
        flash(f'✅ Bot "{bot.name}" ishga tushdi!', 'success')
    else:
        flash(f'❌ Xatolik: {result["error"]}', 'error')
    
    return redirect(url_for('bot.list_bots'))

@bot_control_bp.route('/bot/<int:bot_id>/stop', methods=['POST'])
@login_required
def stop_bot(bot_id):
    """Botni to'xtatish"""
    bot = BotModel.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('Bu bot sizga tegishli emas!', 'error')
        return redirect(url_for('bot.list_bots'))
    
    # Stop bot
    result = polling_manager.stop_bot(bot_id)
    
    if result['success']:
        flash(f'🛑 Bot "{bot.name}" to\'xtatildi!', 'info')
    else:
        flash(f'❌ Xatolik: {result["error"]}', 'error')
    
    return redirect(url_for('bot.list_bots'))

@bot_control_bp.route('/bot/<int:bot_id>/status', methods=['GET'])
@login_required
def bot_status(bot_id):
    """Bot holati"""
    bot = BotModel.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    is_running = polling_manager.is_bot_running(bot_id)
    
    return jsonify({
        'bot_id': bot_id,
        'name': bot.name,
        'is_running': is_running,
        'status': 'Ishlamoqda' if is_running else 'To\'xtatilgan'
    })

@bot_control_bp.route('/bots/status', methods=['GET'])
@login_required
def all_bots_status():
    """Barcha botlar holati"""
    user_bots = BotModel.query.filter_by(user_id=current_user.id).all()
    running_bots = polling_manager.get_running_bots()
    
    bots_status = []
    for bot in user_bots:
        bots_status.append({
            'bot_id': bot.id,
            'name': bot.name,
            'is_running': bot.id in running_bots,
            'has_token': bool(bot.get_telegram_tokens())
        })
    
    return jsonify({
        'bots': bots_status,
        'total_running': len([b for b in bots_status if b['is_running']])
    })
