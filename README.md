# Softwaretechnik-Projekt Data Science SoSe 2024

## Team B

## Setup Server in Ubuntu (Already done)

## How Consumer works

1. 100 Data points are stored inside a list
2. 100 Data points are then stored in the database
3. At the same time, the loss (verlust) check is done which compares the list with the stored data:      
- 1. Compares if the data are same
- 2. Compares if the data are complete
4. The list is the emptied and refilled with next 100 batch of data points
5. Back to 1