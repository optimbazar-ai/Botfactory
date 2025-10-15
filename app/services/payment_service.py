import secrets
from datetime import datetime, timedelta
from flask import current_app


# Subscription plans configuration
SUBSCRIPTION_PLANS = {
    'free': {
        'name': 'Free',
        'name_uz': 'Bepul',
        'name_ru': 'Бесплатный',
        'price': 0,
        'max_bots': 1,
        'features': [
            '1 bot',
            'Basic AI responses',
            'Telegram integration',
            'Community support'
        ],
        'features_uz': [
            '1 ta bot',
            'Asosiy AI javoblar',
            'Telegram integratsiya',
            'Jamoat yordam'
        ]
    },
    'starter': {
        'name': 'Starter',
        'name_uz': 'Starter',
        'name_ru': 'Стартер',
        'price': 165000,  # UZS
        'max_bots': 5,
        'features': [
            '5 bots',
            'Advanced AI responses',
            'Knowledge Base',
            'Priority support',
            '30 days validity'
        ],
        'features_uz': [
            '5 ta bot',
            'Kengaytirilgan AI',
            'Bilimlar bazasi',
            'Tezkor yordam',
            '30 kun amal qiladi'
        ]
    },
    'basic': {
        'name': 'Basic',
        'name_uz': 'Asosiy',
        'name_ru': 'Базовый',
        'price': 290000,  # UZS
        'max_bots': 15,
        'features': [
            '15 bots',
            'Advanced AI + custom models',
            'Unlimited Knowledge Base',
            'Analytics dashboard',
            'Priority support',
            '30 days validity'
        ],
        'features_uz': [
            '15 ta bot',
            'Kengaytirilgan AI',
            'Cheksiz KB',
            'Statistika',
            'Tezkor yordam',
            '30 kun amal qiladi'
        ]
    },
    'premium': {
        'name': 'Premium',
        'name_uz': 'Premium',
        'name_ru': 'Премиум',
        'price': 590000,  # UZS
        'max_bots': 999,
        'features': [
            'Unlimited bots',
            'All AI models',
            'Unlimited Knowledge Base',
            'Advanced analytics',
            'Custom integrations',
            'Dedicated support',
            '30 days validity'
        ],
        'features_uz': [
            'Cheksiz botlar',
            'Barcha AI modellari',
            'Cheksiz KB',
            'To\'liq statistika',
            'Maxsus integratsiyalar',
            'Shaxsiy yordam',
            '30 kun amal qiladi'
        ]
    }
}


def generate_transaction_id():
    """Generate a unique transaction ID."""
    return f"TXN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4).upper()}"


def create_payme_invoice(amount: int, account_id: str):
    """
    Create a PayMe payment invoice (MOCK).
    In production, this would call actual PayMe API.
    
    Args:
        amount: Amount in UZS (sum)
        account_id: User ID or unique identifier
        
    Returns:
        dict: Invoice data with payment URL
    """
    # MOCK implementation
    # In production, you would call PayMe API here
    # https://developer.help.paycom.uz/
    
    transaction_id = generate_transaction_id()
    
    # Mock PayMe payment URL
    # In production: https://checkout.paycom.uz/{encoded_params}
    payme_url = f"https://checkout.paycom.uz/mock?amount={amount}&account={account_id}&transaction={transaction_id}"
    
    return {
        'success': True,
        'transaction_id': transaction_id,
        'payment_url': payme_url,
        'amount': amount,
        'currency': 'UZS',
        'method': 'payme'
    }


def create_click_invoice(amount: int, merchant_user_id: str):
    """
    Create a Click payment invoice (MOCK).
    In production, this would call actual Click API.
    
    Args:
        amount: Amount in UZS (sum)
        merchant_user_id: User ID
        
    Returns:
        dict: Invoice data with payment URL
    """
    # MOCK implementation
    # In production, you would call Click API here
    # https://docs.click.uz/
    
    transaction_id = generate_transaction_id()
    
    # Mock Click payment URL
    # In production: https://my.click.uz/services/pay
    click_url = f"https://my.click.uz/services/pay/mock?amount={amount}&user_id={merchant_user_id}&transaction={transaction_id}"
    
    return {
        'success': True,
        'transaction_id': transaction_id,
        'payment_url': click_url,
        'amount': amount,
        'currency': 'UZS',
        'method': 'click'
    }


def process_test_payment(user, subscription_type: str):
    """
    Process a test payment (for demonstration).
    
    Args:
        user: User model instance
        subscription_type: Type of subscription (starter/basic/premium)
        
    Returns:
        dict: Payment result
    """
    from app.models.payment import Payment
    from app import db
    
    if subscription_type not in SUBSCRIPTION_PLANS or subscription_type == 'free':
        return {
            'success': False,
            'error': 'Invalid subscription type'
        }
    
    plan = SUBSCRIPTION_PLANS[subscription_type]
    
    # Create payment record
    payment = Payment(
        user_id=user.id,
        amount=plan['price'],
        currency='UZS',
        payment_method='test',
        status='completed',
        transaction_id=generate_transaction_id(),
        subscription_type=subscription_type,
        completed_at=datetime.utcnow()
    )
    
    # Update user subscription
    user.subscription_type = subscription_type
    user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
    
    db.session.add(payment)
    db.session.commit()
    
    return {
        'success': True,
        'payment_id': payment.id,
        'transaction_id': payment.transaction_id,
        'subscription_type': subscription_type,
        'valid_until': user.subscription_end_date
    }


def process_payment_webhook(transaction_id: str, status: str):
    """
    Process payment webhook (MOCK).
    In production, this would verify PayMe/Click webhook signatures.
    
    Args:
        transaction_id: Transaction ID from payment gateway
        status: Payment status (completed/failed)
        
    Returns:
        dict: Processing result
    """
    from app.models.payment import Payment
    from app.models.user import User
    from app import db
    
    # Find payment by transaction ID
    payment = Payment.query.filter_by(transaction_id=transaction_id).first()
    
    if not payment:
        return {
            'success': False,
            'error': 'Payment not found'
        }
    
    # Update payment status
    payment.status = status
    
    if status == 'completed':
        payment.completed_at = datetime.utcnow()
        
        # Update user subscription
        user = User.query.get(payment.user_id)
        if user:
            user.subscription_type = payment.subscription_type
            user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
    
    db.session.commit()
    
    return {
        'success': True,
        'payment_id': payment.id,
        'status': payment.status
    }
