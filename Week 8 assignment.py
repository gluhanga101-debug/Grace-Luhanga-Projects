crime_data = [
    ("Downtown",   (25, 28, 22, 30, 27, 21, 24)),
    ("Uptown",     (15, 18, 12, 20, 17, 14, 16)),
    ("Suburbs",    (8, 10, 9, 11, 12, 6, 7)),
    ("Industrial", (12, 14, 11, 16, 13, 10, 9)),
]

def total_crimes_per_district(data):
    """Return [(district, total)] for each district."""
    totals = []
    for district, reports in data:
        totals.append((district, sum(reports)))
    return totals

def worst_crime_district(data):
    """Return (district, total) with highest 7-day total."""
    totals = total_crimes_per_district(data)
    return max(totals, key=lambda x: x[1])

def busiest_crime_day(data):
    """Return (day_index_1_based, total_across_city) with highest citywide count."""
    days = len(data[0][1])
    day_totals = [0] * days
    for _, reports in data:
        for i in range(days):
            day_totals[i] += reports[i]
    best_i = max(range(days), key=lambda i: day_totals[i])
    return best_i + 1, day_totals[best_i]

def pct_change_first_to_last(data):
    """Return [(district, percent_change)] from Day1 to Day7."""
    changes = []
    for district, reports in data:
        first, last = reports[0], reports[-1]
        change = ((last - first) / first) * 100 if first != 0 else 0
        changes.append((district, round(change, 1)))
    return changes

totals = total_crimes_per_district(crime_data)
worst_district_name, worst_total = worst_crime_district(crime_data)
busiest_day, busiest_total = busiest_crime_day(crime_data)
changes = pct_change_first_to_last(crime_data)

print("\nCrime Report Summary (7 days)")
print("-" * 38)
for d, t in totals:
    print(f"{d:<12} : {t:>3} total crimes")
print("-" * 38)
print(f"Worst district (total): {worst_district_name} ({worst_total})")
print(f"Busiest day citywide : Day {busiest_day} ({busiest_total} crimes)")

print("\nFirst→Last Day % Change by District")
print("-" * 38)
for d, pc in changes:
    sign = "+" if pc > 0 else ""
    print(f"{d:<12} : {sign}{pc}%")
print()
