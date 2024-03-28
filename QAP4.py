# QAP 4 Assignment
# One Stop Insurance Company
# Monique Maynard
# March 24, 2024


# Import Datetime
from datetime import datetime, timedelta

# Default values
next_policy_number = 1944
basic_premium = 869.00
discount_additional_cars = 0.25
cost_extra_liability = 130.00
cost_glass_coverage = 86.00
cost_loaner_car = 58.00
hst_rate = 0.15
processing_fee = 39.99

# FormatValues library function
def title_case(value):
    return value.title()

# New FormatValues library function
def uppercase(value):
    return value.upper()

# Function to gather customer information
def gather_customer_info():
    print("Enter customer information:")
    first_name = title_case(input("First Name: "))
    last_name = title_case(input("Last Name: "))
    address = input("Address: ")
    city = title_case(input("City: "))
    provinces = ["ON", "QC", "BC", "AB", "MB", "SK", "NS", "NB", "NL", "PE", "NT", "NU", "YT"]
    province = input("Province ({}): ".format(", ".join(provinces))).upper()
    while province not in provinces:
        province = input("Please enter a valid province: ").upper()
    postal_code = input("Postal Code: ")
    phone_number = input("Phone Number: ")
    num_cars = int(input("Number of Cars: "))
    extra_liability = uppercase(input("Extra Liability Coverage (Y/N): "))
    glass_coverage = uppercase(input("Glass Coverage (Y/N): "))
    loaner_car = uppercase(input("Loaner Car Coverage (Y/N): "))
    payment_method_options = ["FULL", "MONTHLY", "DOWN PAY"]
    payment_method = uppercase(input("Payment Method ({}): ".format(", ".join(payment_method_options))))
    while payment_method not in payment_method_options:
        payment_method = uppercase(input("Please enter a valid payment method: "))
    
    down_payment = 0.00
    if payment_method == "DOWN PAY":
        down_payment = float(input("Enter Down Payment Amount: "))

    # Gather claims information
    claims_dates = []
    claims_costs = []
    while True:
        claim_date_input = input("Enter Claim Date (Press Enter to finish): ")
        if not claim_date_input:
            break
        claim_date = datetime.strptime(claim_date_input, "%Y-%m-%d")
        claim_cost = float(input("Enter Claim Cost: "))
        claims_dates.append(claim_date)
        claims_costs.append(claim_cost)

    return {
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "city": city,
        "province": province,
        "postal_code": postal_code,
        "phone_number": phone_number,
        "num_cars": num_cars,
        "extra_liability": extra_liability,
        "glass_coverage": glass_coverage,
        "loaner_car": loaner_car,
        "payment_method": payment_method,
        "down_payment": down_payment,
        "claims_dates": claims_dates,
        "claims_costs": claims_costs
    }

# Function to calculate insurance premium
def calculate_insurance_premium(customer_info):
    total_premium = basic_premium * (1 + (customer_info["num_cars"] - 1) * discount_additional_cars)

    # Calculate extra costs
    total_extra_costs = 0.00
    if customer_info["extra_liability"] == "Y":
        total_extra_costs += cost_extra_liability * customer_info["num_cars"]
    if customer_info["glass_coverage"] == "Y":
        total_extra_costs += cost_glass_coverage * customer_info["num_cars"]
    if customer_info["loaner_car"] == "Y":
        total_extra_costs += cost_loaner_car * customer_info["num_cars"]

    # Calculate total premium
    total_premium += total_extra_costs

    # Calculate HST
    hst = total_premium * hst_rate

    # Calculate total cost
    total_cost = total_premium + hst

    # Calculate monthly payment
    if customer_info["payment_method"] == "FULL":
        monthly_payment = total_cost / 8
    elif customer_info["payment_method"] == "DOWN PAY":
        remaining_cost = total_cost - customer_info["down_payment"]
        monthly_payment = (remaining_cost + processing_fee) / 8
    else:
        monthly_payment = (total_cost + processing_fee) / 8

    # Calculate invoice date and first payment date
    invoice_date = datetime.now().strftime("%Y-%m-%d")
    first_payment_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    return {
        "total_premium": total_premium,
        "total_extra_costs": total_extra_costs,
        "hst": hst,
        "total_cost": total_cost,
        "monthly_payment": monthly_payment,
        "invoice_date": invoice_date,
        "first_payment_date": first_payment_date
    }

# Function to display customer information and insurance details
def display_customer_info(customer_info, insurance_details):
    print("\nCustomer Information:")
    print(f"Name: {customer_info['first_name']} {customer_info['last_name']}")
    print(f"Address: {customer_info['address']}")
    print(f"City: {customer_info['city']}")
    print(f"Province: {customer_info['province']}")
    print(f"Postal Code: {customer_info['postal_code']}")
    print(f"Phone Number: {customer_info['phone_number']}")
    print(f"Number of Cars: {customer_info['num_cars']}")
    print(f"Extra Liability Coverage: {customer_info['extra_liability']}")
    print(f"Glass Coverage: {customer_info['glass_coverage']}")
    print(f"Loaner Car Coverage: {customer_info['loaner_car']}")
    print(f"Payment Method: {customer_info['payment_method']}")
    if customer_info["payment_method"] == "DOWN PAY":
        print(f"Down Payment: ${customer_info['down_payment']:.2f}")

    print("\nInsurance Details:")
    print(f"Total Premium: ${insurance_details['total_premium']:.2f}")
    print(f"Total Extra Costs: ${insurance_details['total_extra_costs']:.2f}")
    print(f"HST: ${insurance_details['hst']:.2f}")
    print(f"Total Cost: ${insurance_details['total_cost']:.2f}")
    print(f"Monthly Payment: ${insurance_details['monthly_payment']:.2f}")
    print(f"Invoice Date: {insurance_details['invoice_date']}")
    print(f"First Payment Date: {insurance_details['first_payment_date']}")
    print("\nClaims Information:")
    for i in range(len(customer_info["claims_dates"])):
        print(f"Claim Date: {customer_info['claims_dates'][i].strftime('%Y-%m-%d')}, Claim Cost: ${customer_info['claims_costs'][i]:.2f}")

    f = open("ClaimsValues.dat", "a")
 
    f.write("{}, ".format(str(claim_date)))
    f.write("{}\n".format(str(claim_cost)))

    next_policy_number += 1
 
    f.close()

# Main program
while True:
    customer_info = gather_customer_info()
    insurance_details = calculate_insurance_premium(customer_info)
    display_customer_info(customer_info, insurance_details)

    repeat = input("Do you want to enter information for another customer? (Y/N): ")
    if repeat != "Y":
        break