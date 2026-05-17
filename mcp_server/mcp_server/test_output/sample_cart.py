
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.discount_rate = 0
    
    def add_item(self, item, quantity=1):
        """Add an item to the cart"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self.items.append({
            'name': item['name'],
            'price': item['price'],
            'quantity': quantity
        })
    
    def remove_item(self, item_name):
        """Remove an item from the cart"""
        self.items = [item for item in self.items if item['name'] != item_name]
    
    def apply_discount(self, discount_rate):
        """Apply a discount to the cart"""
        if discount_rate < 0 or discount_rate > 1:
            raise ValueError("Discount rate must be between 0 and 1")
        self.discount_rate = discount_rate
    
    def calculate_total(self):
        """Calculate the total price with discount"""
        subtotal = sum(item['price'] * item['quantity'] for item in self.items)
        discount_amount = subtotal * self.discount_rate
        return subtotal - discount_amount
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item['quantity'] for item in self.items)
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.items = []
        self.discount_rate = 0
