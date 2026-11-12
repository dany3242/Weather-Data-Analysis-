weather = {'station':{'1':{'month':{'day':{'temp':111,}}},
                    '2':{'month2':{'day':{'temp':420,}}}}}

stat = 'station'

for i in range (1,len(weather[stat])+1):
    i = str(i)
    for month in weather[stat][i]:
        print(month)
        for day in weather[stat][i][month]:
            print(weather[stat][i][month][day])
            for temp in weather[stat][i][month][day].values():
                print(temp)

nested_dict = {'outer_key': {'inner_key1': 'value1', 'inner_key2': 'value2'}}

for outer_key, inner_dict in nested_dict.items():
    print(f"Outer Key: {outer_key}")
    for inner_key, value in inner_dict.items():
        print(f"Inner Key: {inner_key}, Value: {value}")