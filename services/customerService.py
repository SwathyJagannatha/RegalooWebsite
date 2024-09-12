from database import db
from models.customer import Customer 
from models.order import Order
from sqlalchemy import select
from utils.util import encode_token

def save(customer_data):
    new_customer = Customer(
        name = customer_data['name'],
        email  = customer_data['email'],
        phone = customer_data['phone']
    )

    db.session.add(new_customer)
    # customer_id = new_customer.customer_id --> for sending to front end
    db.session.commit()
    db.session.refresh(new_customer)
    return new_customer 

# retrun jsonify({"message":"New customer sucessfulyy added","customer_id":customer_id}),201

def find_all():
    query = select(Customer)
    all_customers = db.session.execute(query).scalars().all()
    return all_customers

def delete_customer(id):
    query = select(Customer).where(Customer.id == id)
    customer=db.session.execute(query).scalar()

    if customer:
        orders=customer.orders
        for order in orders:
            db.session.delete(order)

        db.session.delete(customer)
        db.session.commit()
        return customer
    else:
        return None

def update_customer(id,data):
    try:
        query = select(Customer).where(Customer.id == id)
        customer=db.session.execute(query).scalar()

        customer.name = data.get("name",customer.name)
        customer.email = data.get("email",customer.email)
        customer.phone = data.get("phone",customer.phone)
        
        db.session.commit()
        return customer 
    except:
        return None
