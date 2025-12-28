from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

pizza_toppings = Table(
    'pizza_toppings',
    Base.metadata,
    Column('pizza_id', Integer, ForeignKey('pizzas.id'), primary_key=True),
    Column('topping_id', Integer, ForeignKey('toppings.id'), primary_key=True)
)

order_pizzas = Table(
    'order_pizzas',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('pizza_id', Integer, ForeignKey('pizzas.id'), primary_key=True),
    Column('quantity', Integer, default=1)
)


class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship('Order', back_populates='customer')
    
    def __repr__(self):
        return f"<Customer(name='{self.name}', email='{self.email}')>"


class Pizza(Base):
    __tablename__ = 'pizzas'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    size = Column(String(20), nullable=False) 
    base_price = Column(Float, nullable=False)
    description = Column(String(500))
    
    toppings = relationship('Topping', secondary=pizza_toppings, back_populates='pizzas')
    orders = relationship('Order', secondary=order_pizzas, back_populates='pizzas')
    
    def __repr__(self):
        return f"<Pizza(name='{self.name}', size='{self.size}', price=${self.base_price})>"


class Topping(Base):
    __tablename__ = 'toppings'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0.0)
    
    pizzas = relationship('Pizza', secondary=pizza_toppings, back_populates='toppings')
    
    def __repr__(self):
        return f"<Topping(name='{self.name}', price=${self.price})>"


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default='pending')
    delivery_address = Column(String(200))
    
    customer = relationship('Customer', back_populates='orders')
    pizzas = relationship('Pizza', secondary=order_pizzas, back_populates='orders')
    
    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, total=${self.total_price}, status='{self.status}')>"
