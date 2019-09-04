from src.tagger.ConnectionHandler import ConnectionHandler

c = ConnectionHandler()

# Present the storm as a number the user can reference quickly
storm_number: int = 1

for storm in c.storm_list:
    print(str(storm_number) + '.  \t' + str(storm))
    storm_number += 1
