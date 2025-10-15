from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.bot import Bot
from app.models.knowledge_base import KnowledgeBase
from app.services.kb_service import process_uploaded_file

kb_bp = Blueprint('kb', __name__, url_prefix='/bots')


@kb_bp.route('/<int:bot_id>/knowledge-base', methods=['GET'])
@login_required
def manage_kb(bot_id):
    """Knowledge base management page for a bot."""
    bot = Bot.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('You do not have permission to access this bot', 'danger')
        return redirect(url_for('bot.list_bots'))
    
    # Get all knowledge bases for this bot
    knowledge_bases = KnowledgeBase.query.filter_by(bot_id=bot_id).order_by(KnowledgeBase.uploaded_at.desc()).all()
    
    return render_template(
        'kb/manage.html',
        bot=bot,
        knowledge_bases=knowledge_bases
    )


@kb_bp.route('/<int:bot_id>/upload-kb', methods=['POST'])
@login_required
def upload_kb(bot_id):
    """Upload a knowledge base file."""
    bot = Bot.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('You do not have permission to access this bot', 'danger')
        return redirect(url_for('bot.list_bots'))
    
    # Check if file is in request
    if 'kb_file' not in request.files:
        flash('No file provided', 'danger')
        return redirect(url_for('kb.manage_kb', bot_id=bot_id))
    
    file = request.files['kb_file']
    
    # Check if file is selected
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('kb.manage_kb', bot_id=bot_id))
    
    try:
        # Process the uploaded file
        file_data = process_uploaded_file(file)
        
        # Create knowledge base record
        kb = KnowledgeBase(
            bot_id=bot_id,
            filename=file_data['filename'],
            content=file_data['content'],
            file_type=file_data['file_type'],
            file_size=file_data['file_size']
        )
        
        db.session.add(kb)
        db.session.commit()
        
        flash(f'Knowledge base "{file_data["filename"]}" uploaded successfully!', 'success')
        
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error uploading file: {str(e)}', 'danger')
    
    return redirect(url_for('kb.manage_kb', bot_id=bot_id))


@kb_bp.route('/<int:bot_id>/kb/<int:kb_id>/delete', methods=['POST'])
@login_required
def delete_kb(bot_id, kb_id):
    """Delete a knowledge base file."""
    bot = Bot.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('You do not have permission to access this bot', 'danger')
        return redirect(url_for('bot.list_bots'))
    
    # Get knowledge base
    kb = KnowledgeBase.query.get_or_404(kb_id)
    
    # Verify it belongs to this bot
    if kb.bot_id != bot_id:
        flash('Invalid knowledge base', 'danger')
        return redirect(url_for('kb.manage_kb', bot_id=bot_id))
    
    filename = kb.filename
    db.session.delete(kb)
    db.session.commit()
    
    flash(f'Knowledge base "{filename}" deleted successfully', 'success')
    return redirect(url_for('kb.manage_kb', bot_id=bot_id))


@kb_bp.route('/<int:bot_id>/kb/<int:kb_id>/view', methods=['GET'])
@login_required
def view_kb(bot_id, kb_id):
    """View knowledge base content."""
    bot = Bot.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('You do not have permission to access this bot', 'danger')
        return redirect(url_for('bot.list_bots'))
    
    # Get knowledge base
    kb = KnowledgeBase.query.get_or_404(kb_id)
    
    # Verify it belongs to this bot
    if kb.bot_id != bot_id:
        flash('Invalid knowledge base', 'danger')
        return redirect(url_for('kb.manage_kb', bot_id=bot_id))
    
    return render_template('kb/view.html', bot=bot, kb=kb)
