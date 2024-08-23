from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import web1 as web
# Configure Selenium WebDriver (make sure you have the appropriate WebDriver executable in your system PATH)
#driver = webdriver.Firefox()

# Open the webpage
url = "https://www.faire.com/discover/melamine-dinnerware"
#driver.get(url)

# Get the page source
#page_source = driver.page_source

# Create a BeautifulSoup object
soup = web.get_content(url)#BeautifulSoup(page_source, "html.parser")

# Find all the product items on the webpage
#product_items = soup.find_all("div", class_="product-item")
product_items = soup.find_all("div", class_="SearchProductsResultsList")
print(product_items)
# Create lists to store the extracted data
product_data = []
for product in product_items:
    # Extract the product name
    #name = product.find("h2", class_="product-title").text.strip()
    name = product.find("strong", class_="product name product-item-name").text.strip()
    print(name)
    # Extract the product price
    price = product.find("span", class_="price").text.strip()
    print(price)

    # Extract the product image URL
    image_url = product.find("img")["src"]

    # Store the data in a dictionary
    product_info = {
        "Name": name,
        "Price": price,
        "Image URL": image_url
    }
    product_data.append(product_info)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(product_data)

# Save the DataFrame to an Excel file
output_file = "scraped_data.xlsx"
df.to_excel(output_file, index=False)

print(f"Data saved to {output_file}")

# Close the WebDriver
driver.quit()

