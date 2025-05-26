# Import testing libraries and webdriver.
import os, pathlib, unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

# Get browser file URI.
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Define web driver.
driver = webdriver.Chrome()

# Define tests.
class WebpageTests(unittest.TestCase):
    def test_title(self):
        driver.get(file_uri('counter.html'))
        self.assertEqual(driver.title, "Counter")
        
    def test_increase(self):
        driver.get(file_uri('counter.html'))
        increase = driver.find_element(By.ID, 'increase')
        increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, 'h1').text, '1')
        
    def test_decrease(self):
        driver.get(file_uri('counter.html'))
        decrease = driver.find_element(By.ID, 'decrease')
        decrease.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, 'h1').text, '-1')
        
    def test_multiple_increase(self):
        driver.get(file_uri('counter.html'))
        increase = driver.find_element(By.ID, 'increase')
        for i in range(3):
            increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, 'h1').text, '3')
        
# Start
if __name__ == '__main__':
    unittest.main()