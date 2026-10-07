from datetime import date, timedelta

from sqlalchemy import select

from app.db.models import (
    Ingredient,
    InventoryBatch,
    InventoryTransaction,
    MenuItem,
    RecipeIngredient,
    Supplier,
    User,
)
from app.db.session import SessionLocal, init_db
from app.services.auth import hash_password

INGREDIENTS = [
    ("Coffee Beans", "kg", 48, 25), ("Milk", "L", 120, 80), ("Sugar", "kg", 22, 15),
    ("Tea Leaves", "kg", 9, 10), ("Chocolate Syrup", "L", 14, 12), ("Caramel Syrup", "L", 6, 10),
    ("Ice Cubes", "kg", 95, 50), ("Croissants", "pcs", 42, 30), ("Cheese", "kg", 8.5, 6),
    ("Tomatoes", "kg", 6.8, 5),
]


def seed() -> None:
    init_db()
    with SessionLocal() as db:
        if db.scalar(select(Ingredient).limit(1)):
            print("Database already contains data; nothing to do.")
            return
        ingredients = {}
        for name, unit, stock, reorder in INGREDIENTS:
            item = Ingredient(name=name, unit=unit, current_stock=stock, reorder_level=reorder, shelf_life_days=7)
            db.add(item)
            ingredients[name] = item
        db.flush()
        menu = [
            ("Cappuccino", "Hot Coffees", 220, [("Coffee Beans", .018), ("Milk", .18), ("Sugar", .01)]),
            ("Cold Brew", "Cold Coffees", 280, [("Coffee Beans", .025), ("Ice Cubes", .15)]),
            ("Masala Chai", "Teas", 140, [("Tea Leaves", .006), ("Milk", .15), ("Sugar", .012)]),
            ("Butter Croissant", "Pastries", 180, [("Croissants", 1)]),
        ]
        for name, category, price, recipe in menu:
            item = MenuItem(name=name, category=category, price=price, description=f"Freshly prepared {name.lower()}.")
            db.add(item)
            db.flush()
            for ingredient, quantity in recipe:
                db.add(RecipeIngredient(menu_item_id=item.id, ingredient_id=ingredients[ingredient].id, quantity=quantity))
        supplier_data = [
            ("BrewCorp", "Coffee Beans", 500, 2, 9.5, 98), ("Highland Roasters", "Coffee Beans", 520, 3, 9.7, 96),
            ("DairyFresh", "Milk", 60, 1, 9.8, 99), ("PureMoo Dairy", "Milk", 55, 1, 9.2, 95),
            ("Assam Tea Co.", "Tea Leaves", 380, 4, 9.6, 97), ("Darjeeling Garden", "Tea Leaves", 420, 5, 9.9, 96),
            ("BakeHouse", "Croissants", 35, 1, 9.4, 97), ("ParisOven", "Croissants", 40, 1, 9.7, 96),
            ("FreshFarms", "Tomatoes", 70, 1, 9.0, 95), ("RedHarvest", "Tomatoes", 65, 2, 8.7, 91),
        ]
        for name, ingredient, price, lead, quality, reliability in supplier_data:
            db.add(Supplier(name=name, ingredient_id=ingredients[ingredient].id, price_per_unit=price, lead_time_days=lead, quality_score=quality, reliability=reliability))
        for item in ingredients.values():
            db.add(InventoryTransaction(ingredient_id=item.id, transaction_type="ADJUSTMENT", quantity=item.current_stock, reason="Initial seed stock"))
            db.add(InventoryBatch(ingredient_id=item.id, lot_number=f"SEED-{item.id:03d}", quantity=item.current_stock, expires_on=date.today() + timedelta(days=item.shelf_life_days)))
        db.add(User(username="manager", password_hash=hash_password("BrewlineDemo123!"), role="manager"))
        db.commit()
        print(f"Seeded {len(ingredients)} ingredients and {len(supplier_data)} suppliers.")


if __name__ == "__main__":
    seed()
