while True:
    try:
        dollars = float(input("Change owed: "))  # Ask user for an amount of change

        if dollars > 0:  # Check user input validity
            break
    except ValueError:
        None

cents = round(dollars * 100)  # Round the change to nearest penny

# Calculate number of largest coins possible
quarter_num = cents // 25
dime_num = (cents % 25) // 10
nikle_num = ((cents % 25) % 10) // 5
penny_num = ((cents % 25) % 10) % 5

coins = quarter_num + dime_num + nikle_num + penny_num

print(coins)