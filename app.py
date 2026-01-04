# app.py - Restaurant Menu Website

from flask import Flask, render_template

# Create the Flask app
app = Flask(__name__)

# Restaurant menu data
menu_data = {
    "restaurant_name": "The Golden Fork",
    "tagline": "Fine Dining Experience",
    "categories": [
        {
            "name": "Appetizers",
            "items": [
                {"name": "Bruschetta", "description": "Grilled bread with fresh tomatoes, basil, and garlic", "price": "8.99"},
                {"name": "Calamari Fritti", "description": "Crispy fried calamari with lemon aioli", "price": "12.99"},
                {"name": "Caesar Salad", "description": "Romaine lettuce, parmesan, croutons, Caesar dressing", "price": "9.99"},
                {"name": "Stuffed Mushrooms", "description": "Button mushrooms filled with herbs and cheese", "price": "10.99"}
            ]
        },
        {
            "name": "Main Courses",
            "items": [
                {"name": "Grilled Salmon", "description": "Atlantic salmon with lemon butter sauce and vegetables", "price": "24.99"},
                {"name": "Ribeye Steak", "description": "12oz premium ribeye with mashed potatoes and asparagus", "price": "32.99"},
                {"name": "Chicken Parmesan", "description": "Breaded chicken breast with marinara and mozzarella", "price": "18.99"},
                {"name": "Lobster Ravioli", "description": "Fresh pasta filled with lobster in creamy sauce", "price": "26.99"},
                {"name": "Vegetable Risotto", "description": "Creamy arborio rice with seasonal vegetables", "price": "16.99"}
            ]
        },
        {
            "name": "Desserts",
            "items": [
                {"name": "Tiramisu", "description": "Classic Italian dessert with coffee and mascarpone", "price": "8.99"},
                {"name": "Chocolate Lava Cake", "description": "Warm chocolate cake with vanilla ice cream", "price": "9.99"},
                {"name": "Crème Brûlée", "description": "Classic French custard with caramelized sugar", "price": "8.99"},
                {"name": "Cheesecake", "description": "New York style cheesecake with berry compote", "price": "7.99"}
            ]
        },
        {
            "name": "Beverages",
            "items": [
                {"name": "Coffee", "description": "Freshly brewed coffee", "price": "3.99"},
                {"name": "Espresso", "description": "Rich Italian espresso", "price": "4.99"},
                {"name": "Fresh Juice", "description": "Orange, apple, or cranberry", "price": "4.99"},
                {"name": "Soft Drinks", "description": "Coca-Cola, Sprite, Fanta", "price": "2.99"},
                {"name": "Iced Tea", "description": "Sweetened or unsweetened", "price": "3.49"}
            ]
        }
    ]
}

# Homepage route
@app.route("/")
def home():
    """Show the restaurant menu"""
    return render_template("index.html", menu=menu_data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)