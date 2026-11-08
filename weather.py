import csv
import matplotlib.pyplot as plt

file_name = "tromsoe_1954_2025_med_makstemperatur.csv"

all_weather_data = {}

chosen_year = input("Enter a year (1954 - 2025): ")

def magnitude(value: str) -> float | None:
    if value.strip() not in ("-", " ", ""):
        return float((value).replace(",", "."))
    else:
        return None

def plot_graf(ax1: int, ax2: int, data_list: list, title: str):
    
    axes[ax1, ax2].plot(range(1, 13), data_list)
    axes[ax1, ax2].set_title(title)
    axes[ax1, ax2].grid()
    axes[ax1, ax2].set_xticks(range(1, 13), months)
    axes[ax1, ax2].fill_between(
        range(1, 13),
        data_list,
        alpha=0.3
    )
    axes[ax1, ax2].set_xlim(1, 12)


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



max_snow_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
tot_precip_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
max_temp_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
min_temp_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
max_wind_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}


for month in valid_values_for_year:
    m_int = int(month) 
   
    max_snow = 0
    if valid_values_for_year[month]["max_snow"]:
        current_max = max(valid_values_for_year[month]["max_snow"])
        max_snow = max(current_max, max_snow)
        max_snow_dict[m_int] = max_snow 

    if valid_values_for_year[month]["tot_precip"] and len(valid_values_for_year[month]["tot_precip"]) > 20:
        total_precip = sum(valid_values_for_year[month]["tot_precip"])
        tot_precip_dict[m_int] = total_precip

    if valid_values_for_year[month]["max_temp"]:
        max_temp_dict[m_int] = max(valid_values_for_year[month]["max_temp"]) # И здесь исправил max_temp вместо avg_temp
        min_temp_dict[m_int] = min(valid_values_for_year[month]["avg_temp"])

    if valid_values_for_year[month]["max_wind"]:
        max_wind_dict[m_int] = max(valid_values_for_year[month]["max_wind"])




months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig, axes = plt.subplots(2, 3, figsize=(14, 8))




plot_graf(0, 0, list(max_snow_dict.values()), "Max Snow Depth (mm)")

plot_graf(0, 1, list(tot_precip_dict.values()), "Total precip. (mm)")

plot_graf(0, 2, list(max_wind_dict.values()), "Max wind (m/s)")

plot_graf(1, 0, list(max_temp_dict.values()), "Max temp (C)")

plot_graf(1, 1, list(min_temp_dict.values()), "Min temp (C)")




summer_days = {}


for year in sorted(all_weather_data[file_name].keys()):
    if year not in summer_days:
        summer_days[year] = {"sd": 0, "hsd": 0, "td": 0}
        
    for month in all_weather_data[file_name][year]:
        for day in all_weather_data[file_name][year][month]:          
            day_data = all_weather_data[file_name][year][month][day]
            

            if day_data["max_temp"] is not None:
                if day_data["max_temp"] >= 30:
                    summer_days[year]["td"] += 1
                elif day_data["max_temp"] >= 25:
                    summer_days[year]["hsd"] += 1
                elif day_data["max_temp"] >= 20:
                    summer_days[year]["sd"] += 1


years_x = [int(y) for y in summer_days] 
sd_y = [data["sd"] for data in summer_days.values()]
hsd_y = [data["hsd"] for data in summer_days.values()]
td_y = [data["td"] for data in summer_days.values()]

ax_six = axes[1, 2]
ax_six.plot(years_x, sd_y, label="20-25°C (Summer)", color="orange")
ax_six.plot(years_x, hsd_y, label="25-30°C (High)", color="red")
ax_six.plot(years_x, td_y, label=">=30°C (Tropic)", color="darkred")

ax_six.set_title("Warm days over the years")
ax_six.grid(True)
ax_six.legend() 


ax_six.set_xlim(min(years_x), max(years_x)) 


plt.tight_layout()
plt.show()
