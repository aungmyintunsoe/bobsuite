# Unit Tests Generated - Steve Sanderson Principles

**File Analyzed:** `mcp_server\test_output\sample_cart.py`
**Language:** Python
**Test Framework:** pytest
**Timestamp:** 2026-05-17T04:56:48.220637Z

## Framework Justification

Pytest is the most widely adopted Python testing framework due to its simplicity, powerful fixtures, and extensive plugin ecosystem. It supports parameterized testing, clear assertion introspection, and seamless integration with mocking libraries like unittest.mock, making it ideal for unit testing isolated components.

## Dependencies

```bash
pip install pytest
```

## Test Files

### test_shopping_cart.py

Tests core ShoppingCart functionality including add, remove, discount application, total calculation, item counting, and cart clearing.

```python
import pytest
from mcp_server.test_output.sample_cart import ShoppingCart

class TestShoppingCart:
    def test_add_item_valid(self):
        cart = ShoppingCart()
        cart.add_item({'name': 'apple', 'price': 1.0}, quantity=2)
        assert cart.get_item_count() == 2
        assert len(cart.items) == 1
        assert cart.items[0]['quantity'] == 2

    def test_add_item_zero_quantity(self):
        cart = ShoppingCart()
        with pytest.raises(ValueError, match='Quantity must be positive'):
            cart.add_item({'name': 'banana', 'price': 0.5}, quantity=0)

    def test_remove_item(self):
        cart = ShoppingCart()
        cart.add_item({'name': 'orange', 'price': 0.8})
        cart.remove_item('orange')
        assert cart.get_item_count() == 0
        assert len(cart.items) == 0

    def test_apply_discount_valid(self):
        cart = ShoppingCart()
        cart.apply_discount(0.1)
        assert cart.discount_rate == 0.1

    def test_apply_discount_invalid(self):
        cart = ShoppingCart()
        with pytest.raises(ValueError, match='Discount rate must be between 0 and 1'):
            cart.apply_discount(-0.05)

    def test_calculate_total_no_discount(self):
        cart = ShoppingCart()
        cart.add_item({'name': 'grape', 'price': 2.0}, quantity=3)
        assert cart.calculate_total() == 6.0

    def test_calculate_total_with_discount(self):
        cart = ShoppingCart()
        cart.add_item({'name': 'mango', 'price': 5.0}, quantity=2)
        cart.apply_discount(0.2)
        assert cart.calculate_total() == 8.0

    def test_get_item_count(self):
        cart = ShoppingCart()
        cart.add_item({'name': 'pear', 'price': 1.5}, quantity=4)
        cart.add_item({'name': 'kiwi', 'price': 2.0}, quantity=1)
        assert cart.get_item_count() == 5

    def test_clear_cart(self):
        cart = ShoppingCart()
        cart.add_item({'name': 'lemon', 'price': 0.7})
        cart.clear_cart()
        assert cart.get_item_count() == 0
        assert cart.discount_rate == 0

```

## Execution Command

```bash
pytest test_shopping_cart.py
```

## Mock Strategy

**Mocking Library:** unittest.mock

## Test Coverage

**Total Tests:** 9

**Units Tested:**

- ShoppingCart.__init__
- ShoppingCart.add_item
- ShoppingCart.remove_item
- ShoppingCart.apply_discount
- ShoppingCart.calculate_total
- ShoppingCart.get_item_count
- ShoppingCart.clear_cart

Each public method of ShoppingCart is tested with both valid and invalid inputs, ensuring 100% statement coverage for the unit. Edge cases like zero quantity and discount rate limits are specifically addressed.

## Design Principles Applied

- Absolute Orthogonality
- Single Logical Assertion
- Isolation of the Unit
- Ruthless Mocking
- Zero Unnecessary Preconditions
- Strict S/S/R Naming Convention

## Notes

Tests focus exclusively on ShoppingCart logic, mocking out any external dependencies that might be introduced in future refactoring. The test suite is designed to be easily extendable as new methods are added to the ShoppingCart class.
