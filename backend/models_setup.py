from ppa import app, db, bcrypt_instance
from ppa.models import PPAUsers, Branches, IndustryTypes

with app.app_context():
    db.create_all()

    
    hashed_pw = bcrypt_instance.generate_password_hash("admin123").decode('utf-8')
    admin_user = PPAUsers(id=1, full_name="admin", email="admin@ppa.com", password_hash=hashed_pw, role="admin")
    db.session.add(admin_user)

    branches_list = [
    "Computer Science and Engineering",
    "Electronics and Communication Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Data Science and Artificial Intelligence"
    ]

    for branch in branches_list:
        branch_row = Branches(branch_name=branch)
        db.session.add(branch_row)
    
    industries_list = [
    "Information Technology & Software Development",
    "Data Analytics & Business Intelligence",
    "Banking, Financial Services & Insurance (BFSI)",
    "Management Consulting",
    "Core Engineering & Manufacturing",
    "Electronics & Semiconductors",
    "EdTech & E-Learning"
    ]

    for industry in industries_list:
        industry_row = IndustryTypes(industry_name=industry)
        db.session.add(industry_row)

    db.session.commit()