import csv
import matplotlib.pyplot as plt

file_name = "oslo_blindern_1954_2025_med_makstemperatur.csv"

all_weather_data = {}

chosen_year = input("Enter a year (1954 - 2025): ")

def magnitude(value: str) -> float | None:
    if value.strip() not in ("-", " ", ""):
        return float((value).replace(",", "."))
    else:
        return None

try:
    with open(file_name, "r", encoding="utf-8") as f:
        data = csv.DictReader(f, delimiter=";")
        
        if file_name not in all_weather_data:
            all_weather_data[file_name] = {}
            for row in data:

                if (not row.get("Tid(norsk normaltid)") or
                "Data er gyldig" in row["Tid(norsk normaltid)"]): continue

                parts = row["Tid(norsk normaltid)"].split('.')
                d = parts[0]
                m = parts[1]
                y = parts[2]

                if not y in all_weather_data[file_name]:
                    all_weather_data[file_name][y] = {}

                if not m in all_weather_data[file_name][y]:
                    all_weather_data[file_name][y][m] = {} 
                            
                if not d in all_weather_data[file_name][y][m]:
                    all_weather_data[file_name][y][m][d] = {
                        "max_temp": magnitude(row["Maksimumstemperatur (døgn)"]),
                        "avg_temp": magnitude(row["Middeltemperatur (døgn)"]),
                        "precip": magnitude(row["Nedbør (døgn)"]),
                        "wind": magnitude(row["Høyeste middelvind (døgn)"]),    
                        "snow": magnitude(row["Snødybde"])                       
                   
                    }

except FileNotFoundError:
    print("Could not find the file.")
    exit()

valid_values_for_year = {}

fn = file_name
cy = chosen_year


for month in all_weather_data[fn][cy]:
    if month not in valid_values_for_year:
        valid_values_for_year[month] = {
            "max_snow": [],
            "tot_precip": [],
            "max_temp": [],
            "avg_temp": [],
            "max_wind": [],                                    
        }

    for day in all_weather_data[fn][cy][month]:  

        day_data = all_weather_data[fn][cy][month][day]  

        if day_data["snow"] is not None:
            valid_values_for_year[month]["max_snow"].append(day_data["snow"])
        if day_data["precip"] is not None:   
            valid_values_for_year[month]["tot_precip"].append(day_data["precip"])
        if day_data["max_temp"] is not None:
            valid_values_for_year[month]["max_temp"].append(day_data["max_temp"])
        if day_data["avg_temp"] is not None:
            valid_values_for_year[month]["avg_temp"].append(day_data["avg_temp"])
        if day_data["wind"] is not None:
            valid_values_for_year[month]["max_wind"].append(day_data["wind"])



max_snow_list = []
tot_precip_list = []
max_temp_list = []
min_temp_list = []
max_wind_list = []


for month in valid_values_for_year:
   
    max_snow = 0

    if valid_values_for_year[month]["max_snow"]:
        current_max = max(valid_values_for_year[month]["max_snow"])
        max_snow = max(current_max, max_snow)
        max_snow_list.append(max_snow)

    if valid_values_for_year[month]["tot_precip"] and len(valid_values_for_year[month]["tot_precip"]) > 20:
        total_precip = sum(valid_values_for_year[month]["tot_precip"])
        tot_precip_list.append(total_precip)
    else:
        tot_precip_list.append(None)

    if valid_values_for_year[month]["max_temp"]:
        max_temp_list.append(max(valid_values_for_year[month]["avg_temp"]))
        min_temp_list.append(min(valid_values_for_year[month]["avg_temp"]))

    if valid_values_for_year[month]["max_wind"]:
        max_wind_list.append(max(valid_values_for_year[month]["max_wind"]))

print(max_snow_list)
print(tot_precip_list)
print(min_temp_list)
print(max_temp_list)
print(max_wind_list)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


fig, axes = plt.subplots(2, 3, figsize=(15, 8))


axes[0, 0].plot(range(1, 13), max_snow_list)
axes[0, 0].set_title("Max Snow Depth (mm)")
axes[0, 0].grid()
axes[0, 0].set_xticks(range(1, 13), months)
axes[0, 0].fill_between(
    range(1, 13),
    max_snow_list,
    alpha=0.3
)
axes[0, 0].set_xlim(1, 12)

axes[0, 1].plot(range(1, 13), tot_precip_list)
axes[0, 1].set_title("Total precip. (mm)")
axes[0, 1].grid()
axes[0, 1].set_xticks(range(1, 13), months)
axes[0, 1].fill_between(
    range(1, 13),
    tot_precip_list,
    alpha=0.3
)
axes[0, 1].set_xlim(1, 12)

axes[0, 2].plot(range(1, 13), max_wind_list)
axes[0, 2].set_title("Max wind (m/s)")
axes[0, 2].grid()
axes[0, 2].set_xticks(range(1, 13), months)
axes[0, 2].fill_between(
    range(1, 13),
    max_wind_list,
    alpha=0.3
)
axes[0, 2].set_xlim(1, 12)

axes[1, 0].plot(range(1, 13), max_temp_list)
axes[1, 0].set_title("Max temp (C)")
axes[1, 0].grid()
axes[1, 0].set_xticks(range(1, 13), months)
axes[1, 0].fill_between(
    range(1, 13),
    max_temp_list,
    alpha=0.3
)
axes[1, 0].set_xlim(1, 12)


axes[1, 1].plot(range(1, 13), min_temp_list)
axes[1, 1].set_title("Min temp (C)")
axes[1, 1].grid()
axes[1, 1].set_xticks(range(1, 13), months)
axes[1, 1].fill_between(
    range(1, 13),
    min_temp_list,
    alpha=0.3
)
axes[1, 1].set_xlim(1, 12)


axes[1, 2].axis("off")

plt.tight_layout()
plt.show()

summer_DAYS = 0
high_summer_DAYS = 0
tropic_DAYS = 0

        
for weather_station in all_weather_data[file_name]:
    for year in all_weather_data[file_name][y]:
        for month in all_weather_data[file_name][y][m]:
            for day in all_weather_data[file_name][y][m][d]:
                for data in all_weather_data[file_name][y][m][d][max_temp]:
                    
                    if data >= 20:
                        summer_DAYS += 1
                    elif data >= 25:
                        high_summer_DAYS += 1
                    elif data >= 30:
                        tropic_DAYS += 1

