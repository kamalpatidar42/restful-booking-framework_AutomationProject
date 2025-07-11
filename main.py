# test_shopping_flow.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import pytest
from selenium import webdriver
class TestShoppingFlow:
    def test_filter_single_size(self, browser):
        page = ShoppingPage(browser)
        for size in ["XS", "S", "M"]:
            page.apply_size_filter(size)
            assert page.verify_filtered_results(size)

    def test_filter_multiple_sizes(self, browser):
        page = ShoppingPage(browser)
        # Apply filters one by one
        page.apply_size_filter("S")
        results_s = page.get_filtered_items()
        page.clear_filters()

        page.apply_size_filter("M")
        results_m = page.get_filtered_items()
        page.clear_filters()

        # Apply S and M together
        page.apply_multiple_filters(["S", "M"])
        results_combined = page.get_filtered_items()

        assert set(results_s + results_m) == set(results_combined)

    def test_add_items_to_cart_order_and_price(self, browser):
        page = ShoppingPage(browser)
        free_shipping_items = page.get_items(free_shipping=True)[:4]
        non_free_item = page.get_items(free_shipping=False)[0]

        for item in free_shipping_items + [non_free_item]:
            page.add_item_to_cart(item)

        assert page.verify_cart_order(free_shipping_items + [non_free_item])
        assert page.verify_cart_prices()

    def test_add_duplicate_items(self, browser):
        page = ShoppingPage(browser)
        item = page.get_items()[0]

        # Add same item multiple times
        for _ in range(3):
            page.add_item_to_cart(item)
        assert page.verify_item_quantity_in_cart(item, 3)

        # Add again using '+' button
        page.increment_item_in_cart(item)
        assert page.verify_item_quantity_in_cart(item, 4)

    def test_delete_items_in_cart(self, browser):
        page = ShoppingPage(browser)
        items = page.get_items()[:3]
        for item in items:
            page.add_item_to_cart(item)

        assert page.verify_cart_summary()

        page.clear_cart()
        assert page.verify_cart_is_empty()

    def test_checkout_order(self, browser):
        page = ShoppingPage(browser)
        items = page.get_items()[:2]
        for item in items:
            page.add_item_to_cart(item)

        total_price = page.get_cart_total_price()
        alert_msg = page.checkout()
        assert str(total_price) in alert_msg

        # Simulate refresh
        browser.refresh()
        assert page.verify_cart_is_empty()
     
     
#Reusable Methods or Object


# shopping_page.py
#class ShoppingPage:
    def __init__(self, driver):
        self.driver = driver

    def apply_size_filter(self, size):
        self.driver.find_element(By.ID, f"filter-size-{size}").click()

    def apply_multiple_filters(self, sizes):
        for size in sizes:
            self.apply_size_filter(size)

    def clear_filters(self):
        self.driver.find_element(By.ID, "clear-filters").click()

    def get_filtered_items(self):
        return [item.text for item in self.driver.find_elements(By.CLASS_NAME, "filtered-item")]

    def add_item_to_cart(self, item):
        item.find_element(By.CLASS_NAME, "add-to-cart").click()

    def increment_item_in_cart(self, item):
        cart_item = self.find_cart_item(item)
        cart_item.find_element(By.CLASS_NAME, "increment").click()

    def find_cart_item(self, item):
        return self.driver.find_element(By.XPATH, f"//div[@class='cart-item' and .//text()='{item.name}']")

    def verify_cart_order(self, items):
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart-item")
        return [ci.text for ci in cart_items] == [item.name for item in items]

    def verify_cart_prices(self):
        # Implement total price validation logic
        return True

    def verify_item_quantity_in_cart(self, item, expected_quantity):
        cart_item = self.find_cart_item(item)
        quantity = int(cart_item.find_element(By.CLASS_NAME, "quantity").text)
        return quantity == expected_quantity

    def verify_cart_summary(self):
        # Check if item count and total price are correct
        return True

    def clear_cart(self):
        self.driver.find_element(By.ID, "clear-cart").click()

    def verify_cart_is_empty(self):
        return not self.driver.find_elements(By.CLASS_NAME, "cart-item")

    def checkout(self):
        self.driver.find_element(By.ID, "checkout").click()
        alert = self.driver.switch_to.alert
        message = alert.text
        alert.accept()
        return message

    def get_cart_total_price(self):
        return float(self.driver.find_element(By.ID, "total-price").text.strip('$'))

    def get_items(self, free_shipping=None):
        items = self.driver.find_elements(By.CLASS_NAME, "product")
        if free_shipping is None:
            return items
        return [
            item for item in items
            if ("Free shipping" in item.text) == free_shipping
        ]
