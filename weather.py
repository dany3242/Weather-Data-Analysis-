import csv
import matplotlib.pyplot as plt

file_name = "venabu_1954_2025_med_makstemperatur.csv"

all_weather_data = {}

chosen_year = input("Enter a year (1954 - 2025): ")

def magnitude(value: str) -> float | None:
    if value.strip() not in ("-", " ", ""):
        return float((value).replace(",", "."))
    else:
        return None

def plot_graf(ax1: int, ax2: int, list: list, title: str):
    
    axes[ax1, ax2].plot(range(1, 13), list)
    axes[ax1, ax2].set_title(title)
    axes[ax1, ax2].grid()
    axes[ax1, ax2].set_xticks(range(1, 13), months)
    axes[ax1, ax2].fill_between(
        range(1, 13),
        list,
        alpha=0.3
    )
    axes[0, 0].set_xlim(1, 12)


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


if not chosen_year in all_weather_data[file_name]:
    print("No data for chosen year")
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



months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig, axes = plt.subplots(2, 3, figsize=(14, 8))

plot_graf(0, 0, max_snow_list, "Max Snow Depth (mm)")
plot_graf(0, 1, tot_precip_list, "Total precip. (mm)")
plot_graf(0, 2, max_wind_list, "Max wind (m/s)")
plot_graf(1, 0, max_temp_list, "Max temp (C)")
plot_graf(1, 1, min_temp_list, "Min temp (C)")
axes[1, 2].axis("off")
plt.tight_layout()
plt.show()