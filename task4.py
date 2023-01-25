# Part 1

'''

Inner Join: Returns records that have matching values in both tables
Left Join: Returns all rows from the left table, even if there are no matches in the right table.
Right Join: Returns all rows from the right table, even if there are no matches in the left table.
Full Join: Combines the results of both left and right outer joins.

'''

# Part 2
import pandas as pd
from pandasql import sqldf

flights = pd.read_csv("candidateEvalData/flights.csv")
airlines = pd.read_csv("candidateEvalData/airlines.csv")

flights_count_df = sqldf(
    """
    SELECT origin, COUNT(*) AS numFlights 
    FROM flights INNER JOIN airlines ON flights.carrier = airlines.carrier 
    WHERE name LIKE '%JetBlue%' 
    GROUP BY origin 
    HAVING numFlights > 100 
    ORDER BY numFlights
    """
)
