from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_session, DATABASE_URL
from models import Customer, Pizza, Topping, Order
from sqlalchemy import func
import os
import sys

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Initialize database on first run
try:
    init_db()
    print("Database initialized successfully", file=sys.stderr)
except Exception as e:
    print(f"Database initialization error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()


@app.route('/')
def index():
    try:
        session = get_session()
        try:
            total_customers = session.query(func.count(Customer.id)).scalar()
            total_pizzas = session.query(func.count(Pizza.id)).scalar()
            total_orders = session.query(func.count(Order.id)).scalar()
            total_revenue = session.query(func.sum(Order.total_price)).scalar() or 0
            
            recent_orders = session.query(Order).order_by(Order.order_date.desc()).limit(5).all()
            
            return render_template('index.html', 
                                 total_customers=total_customers,
                                 total_pizzas=total_pizzas,
                                 total_orders=total_orders,
                                 total_revenue=total_revenue,
                                 recent_orders=recent_orders)
        finally:
            session.close()
    except Exception as e:
        print(f"Error in index route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500


@app.route('/customers')
def customers():
    session = get_session()
    try:
        all_customers = session.query(Customer).all()
        return render_template('customers.html', customers=all_customers)
    finally:
        session.close()


@app.route('/customer/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        session = get_session()
        try:
            new_customer = Customer(
                name=request.form['name'],
                email=request.form['email'],
                phone=request.form['phone'],
                address=request.form['address']
            )
            session.add(new_customer)
            session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers'))
        except Exception as e:
            session.rollback()
            flash(f'Error adding customer: {str(e)}', 'error')
        finally:
            session.close()
    
    return render_template('add_customer.html')


@app.route('/customer/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    session = get_session()
    try:
        customer = session.query(Customer).get(customer_id)
        if customer:
            if customer.orders:
                flash(f'Cannot delete {customer.name}. Customer has {len(customer.orders)} order(s).', 'error')
            else:
                session.delete(customer)
                session.commit()
                flash('Customer deleted successfully!', 'success')
        else:
            flash('Customer not found!', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting customer: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('customers'))


@app.route('/pizzas')
def pizzas():
    session = get_session()
    try:
        all_pizzas = session.query(Pizza).all()
        return render_template('pizzas.html', pizzas=all_pizzas)
    finally:
        session.close()


@app.route('/pizza/add', methods=['GET', 'POST'])
def add_pizza():
    session = get_session()
    try:
        if request.method == 'POST':
            new_pizza = Pizza(
                name=request.form['name'],
                size=request.form['size'],
                base_price=float(request.form['base_price']),
                description=request.form['description']
            )
            
            topping_ids = request.form.getlist('toppings')
            if topping_ids:
                toppings = session.query(Topping).filter(Topping.id.in_(topping_ids)).all()
                new_pizza.toppings.extend(toppings)
            
            session.add(new_pizza)
            session.commit()
            flash('Pizza added successfully!', 'success')
            return redirect(url_for('pizzas'))
        
        all_toppings = session.query(Topping).all()
        return render_template('add_pizza.html', toppings=all_toppings)
    except Exception as e:
        session.rollback()
        flash(f'Error adding pizza: {str(e)}', 'error')
        return redirect(url_for('pizzas'))
    finally:
        session.close()


@app.route('/orders')
def orders():
    session = get_session()
    try:
        all_orders = session.query(Order).order_by(Order.order_date.desc()).all()
        return render_template('orders.html', orders=all_orders)
    finally:
        session.close()


@app.route('/order/add', methods=['GET', 'POST'])
def add_order():
    session = get_session()
    try:
        if request.method == 'POST':
            customer_id = request.form['customer_id']
            pizza_ids = request.form.getlist('pizzas')
            
            if not pizza_ids:
                flash('Please select at least one pizza!', 'error')
                return redirect(url_for('add_order'))
            
            # Calculate total price
            pizzas = session.query(Pizza).filter(Pizza.id.in_(pizza_ids)).all()
            total_price = sum(p.base_price for p in pizzas)
            
            new_order = Order(
                customer_id=customer_id,
                total_price=total_price,
                status=request.form['status'],
                delivery_address=request.form['delivery_address']
            )
            new_order.pizzas.extend(pizzas)
            
            session.add(new_order)
            session.commit()
            flash('Order created successfully!', 'success')
            return redirect(url_for('orders'))
        
        # GET request - show form
        all_customers = session.query(Customer).all()
        all_pizzas = session.query(Pizza).all()
        return render_template('add_order.html', customers=all_customers, pizzas=all_pizzas)
    except Exception as e:
        session.rollback()
        flash(f'Error creating order: {str(e)}', 'error')
        return redirect(url_for('orders'))
    finally:
        session.close()


@app.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    session = get_session()
    try:
        order = session.query(Order).get(order_id)
        if order:
            session.delete(order)
            session.commit()
            flash('Order deleted successfully!', 'success')
        else:
            flash('Order not found!', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting order: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('orders'))


@app.route('/toppings')
def toppings():
    session = get_session()
    try:
        all_toppings = session.query(Topping).all()
        return render_template('toppings.html', toppings=all_toppings)
    finally:
        session.close()


@app.route('/topping/add', methods=['GET', 'POST'])
def add_topping():
    if request.method == 'POST':
        session = get_session()
        try:
            new_topping = Topping(
                name=request.form['name'],
                price=float(request.form['price'])
            )
            session.add(new_topping)
            session.commit()
            flash('Topping added successfully!', 'success')
            return redirect(url_for('toppings'))
        except Exception as e:
            session.rollback()
            flash(f'Error adding topping: {str(e)}', 'error')
        finally:
            session.close()
    
    return render_template('add_topping.html')


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
