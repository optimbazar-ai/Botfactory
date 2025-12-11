"""Create database and admin user"""
from app import app, db, User
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Jadvallar yaratildi!")
    
    # Check if Akramjon001 exists
    user = User.query.filter_by(username='Akramjon001').first()
    
    if user:
        print(f"User mavjud: {user.username}")
        user.password_hash = generate_password_hash('Hisobot201415!')
        user.is_admin = True
        db.session.commit()
        print("✅ Parol yangilandi!")
    else:
        # Create new admin
        new_admin = User(
            username='Akramjon001',
            email='akramjon@botfactory.uz',
            password_hash=generate_password_hash('Hisobot201415!'),
            is_admin=True,
            is_active=True,
            is_premium=True,
            trial_end=datetime.utcnow() + timedelta(days=365)
        )
        db.session.add(new_admin)
        db.session.commit()
        print("✅ Yangi admin yaratildi: Akramjon001")
    
    # Show all users
    print("\nBarcha userlar:")
    for u in User.query.all():
        print(f"  - {u.username} (ID: {u.id}, Admin: {u.is_admin})")
