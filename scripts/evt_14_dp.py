from icecream import ic
import pandas as pd

event21_30 = pd.read_csv("2021_30.csv", usecols=["time", "longitude", "latitude", "depth"])
event21_120 = pd.read_csv("2021_120.csv", usecols=["time", "longitude", "latitude", "depth"])

event = pd.concat([event21_30,event21_120])
event = event.drop_duplicates(keep=False)


event["time"] = event["time"].str.replace("-", "")
event["time"] = event["time"].str.replace(":", "")
event["time"] = event["time"].str.replace("T", "")
event["time"] = event["time"].str[:14]

event.to_csv("event_14depth.csv", header=None, index=None)

event_str = []
with open('event_14depth.csv', 'r', encoding='utf-8') as event_file:
    for line in event_file.readlines():
        event_str.append(line.replace("\n", ""))

for i in event_str:
    with open('event_14_depth.cat', 'a+', encoding='utf-8') as f:
        line = i.replace(",", " ") + "\n"
        f.write(line)

os.remove('event_14depth.csv')
