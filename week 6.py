problems_and_causes = {
    "Shipments delayed": ["Packages not ready on time", "Trucks leaving late", "System errors in dispatch"],
    "Packages not ready on time": ["Too few workers", "Sorting machine breakdown", "Mislabeling of items"],
    "Trucks leaving late": ["Driver shortages", "Traffic congestion", "Late loading process"],
    "System errors in dispatch": ["Outdated software", "Network downtime", "Poor data synchronization"],
    "Too few workers": ["Budget constraints", "High employee turnover"],
    "Sorting machine breakdown": ["Lack of maintenance", "Old equipment"],
    "Mislabeling of items": ["Scanner malfunction", "Inadequate training"],
    "Driver shortages": ["Recruitment delays", "Poor working conditions"]
}

# Step 2: Display initial problems
print("\n Welcome to the Shipment Delay Whys Analysis Tool!")
print("--------------------------------------------------")
print("Possible Problems:")
for key in problems_and_causes.keys():
    print(f"- {key}")

# Step 3: Get initial problem input
initial_problem = input("\nEnter the main problem you want to analyze:\n> ")

if initial_problem not in problems_and_causes:
    print(f"\n Unknown problem. Please choose one from the list above.")
    exit(1)

# Step 4: Show possible causes for the selected problem
causes = problems_and_causes[initial_problem]
print(f"\nPossible Causes for '{initial_problem}':")
for cause in causes:
    print(f"- {cause}")

# Step 5: Continue asking why up to 3 times (simulating the '5 Whys' logic)
why1 = input("\nWhy do you think this happens? Choose from the above causes:\n> ")

if why1 not in problems_and_causes:
    print(f"\nNo deeper causes found for '{why1}'.")
else:
    causes_why1 = problems_and_causes[why1]
    print(f"\nPossible deeper causes for '{why1}':")
    for cause in causes_why1:
        print(f"- {cause}")

    why2 = input("\nWhy do you think that happens?\n> ")

    if why2 in problems_and_causes:
        causes_why2 = problems_and_causes[why2]
        print(f"\nRoot-level causes related to '{why2}':")
        for cause in causes_why2:
            print(f"- {cause}")
    else:
        print(f"\n'{why2}' appears to be a root cause.")

print("\n Analysis complete! You’ve identified a possible chain of causes for shipment delays.")
print("--------------------------------------------------")
print("Tip: Addressing the root cause prevents recurrence of the main issue.\n")