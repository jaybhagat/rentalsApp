from selenium import webdriver
import psycopg2


# getRental(url, prices_arr, addresses_arr, beds_arr, baths_arr, sqft_arr,
#   pets_arr, type_arr, updated_arr, contacts_arr) scrapes the url given and
#   modifies the arrays given with the new information scraped.
# effects: modifies arrays passed
# time: O(n^2) where n is the max of the items found

def getRental(url, prices_arr, addresses_arr, beds_arr, baths_arr, sqft_arr, pets_arr, type_arr, updated_arr, contacts_arr):
    chrome_path = "/Users/jay/Documents/Code/python/webscraperApp/chromedriver"
    driver = webdriver.Chrome(chrome_path)

    driver.get(url) # openinng browser

    # getting prices
    prices = driver.find_elements_by_xpath('//p[@class="listing-card__price"]')
    for price in prices:
        prices_arr.append(price.text)

    # getting addresses
    addresses = driver.find_elements_by_xpath('//h2[@class="listing-card__title"]')
    for address in addresses:
        addresses_arr.append(address.text)

    # getting bedrooms, bathrooms, area, pets policies
    details = driver.find_elements_by_xpath('//ul[@class="listing-card__main-features"]')
    for detail in details:
        if "BED" not in detail.text:
            beds_arr.append(-1)
        if "BATH" not in detail.text:
            baths_arr.append(-1)
        if "FT" not in detail.text:
            sqft_arr.append(-1)
        if "PETS" not in detail.text:
            pets_arr.append(0)

        details_split = detail.text.split('\n')
        for item in details_split:
            if("BED" in item):
                beds_arr.append(item)
            elif ("BATH" in item):
                baths_arr.append(item)
            elif ("FT" in item):
                sqft_arr.append(item)
            elif ("PETS" in item):
                pets_arr.append(1)

    # getting type of rental and last time it was updated
    type_updateds = driver.find_elements_by_xpath('//div[@class="listing-card__type-and-updated"]')
    for type_updated in type_updateds:
        type_and_updated = type_updated.text.split('\n')
        type_arr.append(type_and_updated[0])
        updated_arr.append(type_and_updated[1])

    # getting the contact information of each rental
    contacts = driver.find_elements_by_xpath('//a[@class="listing-card__permalink-button btn-cta btn-cta--primary"]')
    for contact in contacts:
        contacts_arr.append(contact.get_attribute('href'))

    driver.close()

# arrays for each specification
prices = []
addresses = []
beds = []
baths = []
sqft = []
pets = []
types = []
updateds = []
contacts = []

# websites to scrape
def scrapeWeb():
    for i in range(0,61):
        getRental("https://rentals.ca/toronto?p={}".format(i), prices, addresses, beds, baths, sqft, pets, types, updateds, contacts)

scrapeWeb()

# splitting values that only require numbers
for i in range(len(prices)):
    prices[i] = int((prices[i].split('$')[1]).split()[0])

for i in range(len(beds)):
    beds[i] = float(beds[i].split()[0])

for i in range(len(baths)):
    baths[i] = float(baths[i].split()[0])

for i in range(len(sqft)):
    sqft[i] = int(str(sqft[i]).split()[0])


# connecting to PostgreSQL to create a table
db_connection = psycopg2.connect(
    database="rentalInfo",
    user="jay",
    password="",
    host="127.0.0.1",
    port="5432"
)

cursor = db_connection.cursor()

for i in range(len(prices)):
    cursor.execute('''INSERT INTO rentals (address, price, beds, baths, sqft, \
    pets, types, last_updated, contact_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', \
    (addresses[i], prices[i], beds[i], baths[i], sqft[i], pets[i], types[i], updateds[i], contacts[i]))

cursor.close()
db_connection.commit()
