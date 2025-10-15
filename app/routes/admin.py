from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app import db
from app.models.user import User
from app.models.bot import Bot
from app.models.payment import Payment
from app.models.knowledge_base import KnowledgeBase
from app.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard overview with statistics."""
    # User statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    # Subscription statistics
    free_users = User.query.filter_by(subscription_type='free').count()
    starter_users = User.query.filter_by(subscription_type='starter').count()
    basic_users = User.query.filter_by(subscription_type='basic').count()
    premium_users = User.query.filter_by(subscription_type='premium').count()
    
    # Bot statistics
    total_bots = Bot.query.count()
    active_bots = Bot.query.filter_by(is_active=True).count()
    bots_with_kb = db.session.query(Bot.id).join(KnowledgeBase).distinct().count()
    
    # Payment statistics
    total_payments = Payment.query.count()
    completed_payments = Payment.query.filter_by(status='completed').count()
    
    # Revenue statistics
    total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0
    
    # Recent activity
    recent_users = User.query.order_by(desc(User.created_at)).limit(5).all()
    recent_payments = Payment.query.order_by(desc(Payment.created_at)).limit(5).all()
    recent_bots = Bot.query.order_by(desc(Bot.created_at)).limit(5).all()
    
    # Monthly registration data (last 6 months)
    monthly_data = []
    for i in range(5, -1, -1):
        start_date = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
        end_date = start_date + timedelta(days=30)
        count = User.query.filter(User.created_at >= start_date, User.created_at < end_date).count()
        monthly_data.append({
            'month': start_date.strftime('%b %Y'),
            'count': count
        })
    
    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        active_users=active_users,
        admin_users=admin_users,
        free_users=free_users,
        starter_users=starter_users,
        basic_users=basic_users,
        premium_users=premium_users,
        total_bots=total_bots,
        active_bots=active_bots,
        bots_with_kb=bots_with_kb,
        total_payments=total_payments,
        completed_payments=completed_payments,
        total_revenue=total_revenue,
        recent_users=recent_users,
        recent_payments=recent_payments,
        recent_bots=recent_bots,
        monthly_data=monthly_data
    )


@admin_bp.route('/users')
@admin_required
def users():
    """List all users with search and filter."""
    # Get filters from query params
    search = request.args.get('search', '').strip()
    subscription_filter = request.args.get('subscription', '')
    status_filter = request.args.get('status', '')
    
    # Build query
    query = User.query
    
    # Apply search
    if search:
        query = query.filter(
            (User.username.contains(search)) |
            (User.email.contains(search))
        )
    
    # Apply subscription filter
    if subscription_filter:
        query = query.filter_by(subscription_type=subscription_filter)
    
    # Apply status filter
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'inactive':
        query = query.filter_by(is_active=False)
    elif status_filter == 'admin':
        query = query.filter_by(is_admin=True)
    
    # Order by creation date (newest first)
    users = query.order_by(desc(User.created_at)).all()
    
    return render_template(
        'admin/users.html',
        users=users,
        search=search,
        subscription_filter=subscription_filter,
        status_filter=status_filter
    )


@admin_bp.route('/bots')
@admin_required
def bots():
    """List all bots with search and filter."""
    # Get filters
    search = request.args.get('search', '').strip()
    platform_filter = request.args.get('platform', '')
    status_filter = request.args.get('status', '')
    
    # Build query
    query = Bot.query.join(User)
    
    # Apply search
    if search:
        query = query.filter(
            (Bot.name.contains(search)) |
            (User.username.contains(search))
        )
    
    # Apply platform filter
    if platform_filter:
        query = query.filter(Bot.platform == platform_filter)
    
    # Apply status filter
    if status_filter == 'active':
        query = query.filter(Bot.is_active == True)
    elif status_filter == 'inactive':
        query = query.filter(Bot.is_active == False)
    
    # Order by creation date
    bots = query.order_by(desc(Bot.created_at)).all()
    
    return render_template(
        'admin/bots.html',
        bots=bots,
        search=search,
        platform_filter=platform_filter,
        status_filter=status_filter
    )


@admin_bp.route('/payments')
@admin_required
def payments():
    """List all payments with filters."""
    # Get filters
    method_filter = request.args.get('method', '')
    status_filter = request.args.get('status', '')
    
    # Build query
    query = Payment.query.join(User)
    
    # Apply method filter
    if method_filter:
        query = query.filter(Payment.payment_method == method_filter)
    
    # Apply status filter
    if status_filter:
        query = query.filter(Payment.status == status_filter)
    
    # Order by creation date
    payments = query.order_by(desc(Payment.created_at)).all()
    
    # Calculate totals
    total_amount = sum(p.amount for p in payments if p.status == 'completed')
    
    return render_template(
        'admin/payments.html',
        payments=payments,
        method_filter=method_filter,
        status_filter=status_filter,
        total_amount=total_amount
    )


@admin_bp.route('/user/<int:user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    """Deactivate or activate a user."""
    user = User.query.get_or_404(user_id)
    
    # Prevent deactivating yourself
    from flask_login import current_user
    if user.id == current_user.id:
        flash('You cannot deactivate yourself!', 'danger')
        return redirect(url_for('admin.users'))
    
    # Toggle active status
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}', 'success')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/user/<int:user_id>/extend-subscription', methods=['POST'])
@admin_required
def extend_subscription(user_id):
    """Extend user's subscription by 30 days."""
    user = User.query.get_or_404(user_id)
    
    if user.subscription_type == 'free':
        flash('Cannot extend free plan subscription', 'warning')
        return redirect(url_for('admin.users'))
    
    # If subscription is active, extend from end date, otherwise from now
    if user.subscription_end_date and user.subscription_end_date > datetime.utcnow():
        user.subscription_end_date = user.subscription_end_date + timedelta(days=30)
    else:
        user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
    
    db.session.commit()
    
    flash(f'Subscription extended for {user.username} until {user.subscription_end_date.strftime("%Y-%m-%d")}', 'success')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/user/<int:user_id>/make-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    """Toggle admin status for a user."""
    user = User.query.get_or_404(user_id)
    
    from flask_login import current_user
    if user.id == current_user.id:
        flash('You cannot change your own admin status!', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for {user.username}', 'success')
    
    return redirect(url_for('admin.users'))
