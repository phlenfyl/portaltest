import pandas as pd

# Read the text file
with open('/Users/richardbuehling/Desktop/The357CompanyPortal/portal/main/carriers.txt', 'r') as file:
    lines = file.readlines()

# Lists to store parsed data
names = []
addresses = []
cities = []
states = []
zip_codes = []
insurances = []
drivers = []
airports = []

# Iterate through the lines and extract data
i = 0
while i < len(lines):
    # Carrier Name
    names.append(lines[i].strip())
    i += 1

    # Address, City, State, ZIP Code
    addr, city_state_zip = lines[i].split(',')
    addresses.append(addr.strip())
    city, rest = city_state_zip.strip().rsplit(' ', 1)
    print(rest)
    state, zip_code = rest.split(' - ')
    cities.append(city)
    states.append(state)
    zip_codes.append(zip_code)
    i += 1

    # General Liability Insurance and Number of Drivers
    insurance = None
    number_of_drivers = None
    while 'Approximate # Of Drivers:' not in lines[i]:
        if 'General Liability Insurance:' in lines[i]:
            insurance = lines[i].split(':')[-1].strip()
        i += 1

    number_of_drivers = lines[i].split(':')[-1].strip()
    insurances.append(insurance)
    drivers.append(number_of_drivers)
    i += 1

    # Airports Served
    if i < len(lines) and 'Airports Served:' in lines[i]:
        airports.append(lines[i].split(':')[-1].strip())
        i += 1
    else:
        airports.append(None)

df = pd.DataFrame({
    'Carrier Name': names,
    'Address': addresses,
    'City': cities,
    'State': states,
    'ZIP Code': zip_codes,
    'General Liability Insurance Amount': insurances,
    'Approximate Number of Drivers': drivers,
    'Airports Served': airports
})

# Save to Excel
df.to_excel("carriers.xlsx", index=False)
