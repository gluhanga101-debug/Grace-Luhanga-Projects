training_data = [120, 130, 140, 125, 110, 90, 85, 95, 115, 130]

drop_count = 0
max_increase = 0
max_increase_day = 0
top_days = sorted(training_data, reverse=True)[:3]

for i in range(1, len(training_data)):
    # Check for performance drops
    if training_data[i] < training_data[i - 1]:
        drop_count += 1

    # Find the biggest single-day improvement
    increase = training_data[i] - training_data[i - 1]
    if increase > max_increase:
        max_increase = increase
        max_increase_day = i + 1  

print(f"Number of days with performance drop: {drop_count}")
print(f"Biggest single-day improvement: {max_increase} punches (Day {max_increase_day})")
print(f"Top three best-performing days: {top_days}")
