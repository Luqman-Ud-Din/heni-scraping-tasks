# Part 1

'''

Inner Join: Returns records that have matching values in both tables
Left Join: Returns all rows from the left table, even if there are no matches in the right table.
Right Join: Returns all rows from the right table, even if there are no matches in the left table.
Full Join: Combines the results of both left and right outer joins.

'''

# Part 2
import pandas as pd

flights = pd.read_csv("candidateEvalData/flights.csv")
airlines = pd.read_csv("candidateEvalData/airlines.csv")

# Add full airline name to the flights dataframe and show the arr_time, origin, dest and the name of the airline.
result_df = flights.merge(airlines, on='carrier')[['arr_time', 'origin', 'dest', 'name']]

# Filter resulting data.frame to include only flights containing the word JetBlue
jet_blue_df = result_df[result_df.name.str.contains('JetBlue', na=False)]

# Summarise the total number of flights by origin in ascending.
flight_count_by_origin_series = jet_blue_df.groupby('origin').size().sort_values(ascending=True)
flights_count_df = pd.DataFrame({'numFlights': flight_count_by_origin_series}).reset_index()

# Filter resulting data.frame to return only origins with more than 100
filtered_flights_count_df = flights_count_df[flights_count_df['numFlights'] > 100]
