from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.payment import Payment
from app.services.payment_service import (
    SUBSCRIPTION_PLANS,
    create_payme_invoice,
    create_click_invoice,
    process_test_payment,
    process_payment_webhook
)

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')


@payment_bp.route('/subscribe')
@login_required
def subscribe():
    """Show subscription plans."""
    # Get user's current subscription
    current_plan = current_user.subscription_type
    
    # Check if subscription is active
    subscription_active = current_user.is_subscription_active()
    
    return render_template(
        'payment/subscribe.html',
        plans=SUBSCRIPTION_PLANS,
        current_plan=current_plan,
        subscription_active=subscription_active
    )


@payment_bp.route('/payme/create', methods=['POST'])
@login_required
def create_payme_payment():
    """Create PayMe payment invoice."""
    subscription_type = request.form.get('subscription_type')
    
    if not subscription_type or subscription_type not in SUBSCRIPTION_PLANS:
        flash('Invalid subscription plan selected', 'danger')
        return redirect(url_for('payment.subscribe'))
    
    if subscription_type == 'free':
        flash('Free plan does not require payment', 'info')
        return redirect(url_for('payment.subscribe'))
    
    plan = SUBSCRIPTION_PLANS[subscription_type]
    
    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        amount=plan['price'],
        currency='UZS',
        payment_method='payme',
        status='pending',
        subscription_type=subscription_type
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # Create PayMe invoice
    invoice = create_payme_invoice(
        amount=plan['price'],
        account_id=str(current_user.id)
    )
    
    # Update payment with transaction ID
    payment.transaction_id = invoice['transaction_id']
    db.session.commit()
    
    # In production, redirect to PayMe checkout
    # return redirect(invoice['payment_url'])
    
    # For demo, show the payment URL
    flash(f'PayMe payment created. Transaction ID: {invoice["transaction_id"]}', 'info')
    flash(f'In production, you would be redirected to: {invoice["payment_url"]}', 'warning')
    
    return redirect(url_for('payment.payment_status', payment_id=payment.id))


@payment_bp.route('/click/create', methods=['POST'])
@login_required
def create_click_payment():
    """Create Click payment invoice."""
    subscription_type = request.form.get('subscription_type')
    
    if not subscription_type or subscription_type not in SUBSCRIPTION_PLANS:
        flash('Invalid subscription plan selected', 'danger')
        return redirect(url_for('payment.subscribe'))
    
    if subscription_type == 'free':
        flash('Free plan does not require payment', 'info')
        return redirect(url_for('payment.subscribe'))
    
    plan = SUBSCRIPTION_PLANS[subscription_type]
    
    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        amount=plan['price'],
        currency='UZS',
        payment_method='click',
        status='pending',
        subscription_type=subscription_type
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # Create Click invoice
    invoice = create_click_invoice(
        amount=plan['price'],
        merchant_user_id=str(current_user.id)
    )
    
    # Update payment with transaction ID
    payment.transaction_id = invoice['transaction_id']
    db.session.commit()
    
    # In production, redirect to Click checkout
    # return redirect(invoice['payment_url'])
    
    # For demo, show the payment URL
    flash(f'Click payment created. Transaction ID: {invoice["transaction_id"]}', 'info')
    flash(f'In production, you would be redirected to: {invoice["payment_url"]}', 'warning')
    
    return redirect(url_for('payment.payment_status', payment_id=payment.id))


@payment_bp.route('/test/create', methods=['POST'])
@login_required
def create_test_payment():
    """Create a test payment (for demonstration purposes)."""
    subscription_type = request.form.get('subscription_type')
    
    if not subscription_type or subscription_type not in SUBSCRIPTION_PLANS:
        flash('Invalid subscription plan selected', 'danger')
        return redirect(url_for('payment.subscribe'))
    
    if subscription_type == 'free':
        flash('Already on free plan', 'info')
        return redirect(url_for('payment.subscribe'))
    
    # Process test payment
    result = process_test_payment(current_user, subscription_type)
    
    if result['success']:
        flash(f'✅ Test payment successful! Subscription upgraded to {subscription_type.capitalize()}', 'success')
        flash(f'Valid until: {result["valid_until"].strftime("%Y-%m-%d")}', 'info')
        return redirect(url_for('auth.index'))
    else:
        flash(f'Payment failed: {result.get("error")}', 'danger')
        return redirect(url_for('payment.subscribe'))


@payment_bp.route('/status/<int:payment_id>')
@login_required
def payment_status(payment_id):
    """Show payment status."""
    payment = Payment.query.get_or_404(payment_id)
    
    # Check ownership
    if payment.user_id != current_user.id:
        flash('You do not have permission to view this payment', 'danger')
        return redirect(url_for('payment.subscribe'))
    
    return render_template('payment/status.html', payment=payment)


@payment_bp.route('/webhook/<method>', methods=['POST'])
def payment_webhook(method):
    """
    Payment webhook endpoint (for PayMe/Click callbacks).
    In production, this would verify webhook signatures.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    transaction_id = data.get('transaction_id')
    status = data.get('status', 'completed')
    
    if not transaction_id:
        return jsonify({'error': 'Transaction ID required'}), 400
    
    # Process webhook
    result = process_payment_webhook(transaction_id, status)
    
    if result['success']:
        return jsonify({'success': True, 'payment_id': result['payment_id']})
    else:
        return jsonify({'success': False, 'error': result.get('error')}), 404


@payment_bp.route('/history')
@login_required
def payment_history():
    """Show user's payment history."""
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.created_at.desc()).all()
    
    return render_template('payment/history.html', payments=payments)


@payment_bp.route('/simulate-webhook/<int:payment_id>')
@login_required
def simulate_webhook(payment_id):
    """Simulate a successful payment webhook (for testing)."""
    payment = Payment.query.get_or_404(payment_id)
    
    # Check ownership
    if payment.user_id != current_user.id:
        flash('You do not have permission to access this payment', 'danger')
        return redirect(url_for('payment.subscribe'))
    
    if payment.status == 'completed':
        flash('Payment already completed', 'info')
        return redirect(url_for('payment.payment_status', payment_id=payment_id))
    
    # Simulate successful webhook
    result = process_payment_webhook(payment.transaction_id, 'completed')
    
    if result['success']:
        flash('✅ Payment webhook simulated successfully! Subscription activated.', 'success')
    else:
        flash('Failed to process webhook', 'danger')
    
    return redirect(url_for('payment.payment_status', payment_id=payment_id))
