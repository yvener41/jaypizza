from database import init_db, get_session
from models import Customer, Pizza, Topping, Order

def populate_sample_data():
    """Populate the database with sample data"""
    session = get_session()
    
    try:
        toppings = [
            Topping(name="Pepperoni", price=1.50),
            Topping(name="Mushrooms", price=1.00),
            Topping(name="Olives", price=1.00),
            Topping(name="Extra Cheese", price=2.00),
            Topping(name="Sausage", price=1.50),
            Topping(name="Bell Peppers", price=1.00),
            Topping(name="Onions", price=0.75),
        ]
        session.add_all(toppings)
        
        margherita = Pizza(
            name="Margherita",
            size="Medium",
            base_price=10.99,
            description="Classic pizza with tomato sauce, mozzarella, and basil"
        )
        
        pepperoni_pizza = Pizza(
            name="Pepperoni Special",
            size="Large",
            base_price=14.99,
            description="Loaded with pepperoni and extra cheese"
        )
        pepperoni_pizza.toppings.extend([toppings[0], toppings[3]]) 
        
        veggie_pizza = Pizza(
            name="Veggie Delight",
            size="Medium",
            base_price=12.99,
            description="Healthy pizza with mushrooms, olives, peppers, and onions"
        )
        veggie_pizza.toppings.extend([toppings[1], toppings[2], toppings[5], toppings[6]])
        
        session.add_all([margherita, pepperoni_pizza, veggie_pizza])
        
        # Create customers
        customer1 = Customer(
            name="John Doe",
            email="john.doe@example.com",
            phone="555-0101",
            address="123 Main St, Anytown, USA"
        )
        
        customer2 = Customer(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="555-0102",
            address="456 Oak Ave, Somewhere, USA"
        )
        
        session.add_all([customer1, customer2])
        
        # Create orders
        order1 = Order(
            customer=customer1,
            total_price=25.98,
            status="delivered",
            delivery_address=customer1.address
        )
        order1.pizzas.extend([margherita, pepperoni_pizza])
        
        order2 = Order(
            customer=customer2,
            total_price=12.99,
            status="preparing",
            delivery_address=customer2.address
        )
        order2.pizzas.append(veggie_pizza)
        
        session.add_all([order1, order2])
        
        session.commit()
        print("Sample data added successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error adding sample data: {e}")
    finally:
        session.close()


def display_data():
    """Display all data in the database"""
    session = get_session()
    
    try:
        print("\n=== CUSTOMERS ===")
        customers = session.query(Customer).all()
        for customer in customers:
            print(customer)
        
        print("\n=== TOPPINGS ===")
        toppings = session.query(Topping).all()
        for topping in toppings:
            print(topping)
        
        print("\n=== PIZZAS ===")
        pizzas = session.query(Pizza).all()
        for pizza in pizzas:
            print(f"{pizza}")
            if pizza.toppings:
                print(f"  Toppings: {', '.join([t.name for t in pizza.toppings])}")
        
        print("\n=== ORDERS ===")
        orders = session.query(Order).all()
        for order in orders:
            print(f"{order}")
            print(f"  Customer: {order.customer.name}")
            print(f"  Pizzas: {', '.join([p.name for p in order.pizzas])}")
        
    finally:
        session.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    
    print("\nAdding sample data...")
    populate_sample_data()
    
    print("\nDisplaying database contents...")
    display_data()
