import os
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
faker = Faker()

# Folder for saving datasets
output_folder = "synthetic_datasets"
os.makedirs(output_folder, exist_ok=True)

# Dataset creation functions
def generate_customers(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "customer_id": faker.uuid4(),
            "name": faker.name(),
            "email": faker.email(),
            "phone": faker.phone_number(),
            "location": faker.address(),
            "signup_date": faker.date_between(start_date="-2y", end_date="today"),
            "is_premium": faker.boolean(),
            "preferred_cuisine": random.choice(["Indian", "Chinese", "Mexican", "Italian", "American"]),
            "total_orders": random.randint(1, 50),
            "average_rating": round(random.uniform(1, 5), 2)
        })
    return pd.DataFrame(data)

def generate_restaurants(num_records=50):
    data = []
    for _ in range(num_records):
        data.append({
            "restaurant_id": faker.uuid4(),
            "name": faker.company(),
            "cuisine_type": random.choice(["Indian", "Chinese", "Mexican", "Italian", "American"]),
            "location": faker.address(),
            "owner_name": faker.name(),
            "average_delivery_time": random.randint(20, 60),
            "contact_number": faker.phone_number(),
            "rating": round(random.uniform(1, 5), 2),
            "total_orders": random.randint(1, 200),
            "is_active": faker.boolean()
        })
    return pd.DataFrame(data)

def generate_orders(num_records=200, customer_ids=None, restaurant_ids=None):
    data = []
    for _ in range(num_records):
        customer_id = random.choice(customer_ids) if customer_ids else faker.uuid4()
        restaurant_id = random.choice(restaurant_ids) if restaurant_ids else faker.uuid4()
        order_date = faker.date_time_between(start_date="-1y", end_date="now")
        delivery_time = order_date + timedelta(minutes=random.randint(20, 120))
        status = random.choice(["Pending", "Delivered", "Cancelled"])
        total_amount = round(random.uniform(10, 200), 2)
        data.append({
            "order_id": faker.uuid4(),
            "customer_id": customer_id,
            "restaurant_id": restaurant_id,
            "order_date": order_date,
            "delivery_time": delivery_time if status == "Delivered" else None,
            "status": status,
            "total_amount": total_amount,
            "payment_mode": random.choice(["Credit Card", "Cash", "UPI"]),
            "discount_applied": round(random.uniform(0, 20), 2),
            "feedback_rating": round(random.uniform(1, 5), 2)
        })
    return pd.DataFrame(data)

def generate_deliveries(num_records=200, order_ids=None):
    data = []
    for _ in range(num_records):
        order_id = random.choice(order_ids) if order_ids else faker.uuid4()
        delivery_status = random.choice(["On the way", "Delivered"])
        actual_delivery_time = random.randint(15, 120)
        estimated_time = actual_delivery_time + random.randint(-10, 10)
        data.append({
            "delivery_id": faker.uuid4(),
            "order_id": order_id,
            "delivery_status": delivery_status,
            "distance": round(random.uniform(1, 20), 2),
            "delivery_time": actual_delivery_time,
            "estimated_time": estimated_time,
            "delivery_fee": round(random.uniform(2, 10), 2),
            "vehicle_type": random.choice(["Bike", "Car", "Scooter"])
        })
    return pd.DataFrame(data)

# Generate datasets
customers_df = generate_customers(100)
restaurants_df = generate_restaurants(50)
orders_df = generate_orders(200, customers_df["customer_id"].tolist(), restaurants_df["restaurant_id"].tolist())
deliveries_df = generate_deliveries(200, orders_df["order_id"].tolist())

# Save datasets as CSV files
customers_file = os.path.join(output_folder, "customers.csv")
restaurants_file = os.path.join(output_folder, "restaurants.csv")
orders_file = os.path.join(output_folder, "orders.csv")
deliveries_file = os.path.join(output_folder, "deliveries.csv")

customers_df.to_csv(customers_file, index=False)
restaurants_df.to_csv(restaurants_file, index=False)
orders_df.to_csv(orders_file, index=False)
deliveries_df.to_csv(deliveries_file, index=False)

print(f"Datasets saved in folder: {output_folder}")
