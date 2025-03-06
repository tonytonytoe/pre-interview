from z3 import * 
import os
import time
import csv

# Find the queries folder
folder_path = "queries"


# Returns a list of the names of the entries in a directory
try:
  files = os.listdir(folder_path)
except FileNotFoundError:
  # If the queries folder cannot be found
  print(f"Error: Folder not found at {folder_path}")
  exit()




# Goes through each file in the list that was made from the queries folder
for file_name in files:
  # Creates path from the queries folder to the file
  file_path = os.path.join(folder_path, file_name)
  if os.path.isfile(file_path):  # Ensure it's a file, not a subfolder
      # Open and process the file
      try:
          # 'r' for reading file
          with open(file_path, 'r') as file:
              # Read file
              content = file.read()
              # Run smt test
              print(f"Processing file: {file_name}")
              # Logic
              f = parse_smt2_string(content)
              solver = Solver()
              #start the timer
              start_time = time.time()
              #set a time out limit
              solver.set("timeout",60000)
              result = solver.check(f)
              #stop the timer
              end_time = time.time()
              elapsed = round(end_time-start_time,2)
              # Get the results
              if result == sat:
                  print("The problem is satisfiable!")
                  print(f"elapsed time: {elapsed}")
                  res = "SAT"

              elif result == unsat:
                  print("The problem is unsatisfiable.")
                  print(f"elapsed time: {end_time-start_time}")
                  res = "UNSAT"
              else:
                  print(f"Solving timed out after {60000} milliseconds.")
                  res = "TIMEOUT"
              #this is the data being appended to the results.csv file
              data_to_append = [file_name,res,elapsed]
              
              file_path = 'results.csv'
              #open the results file and add a new line of all 3 data values
              with open(file_path, 'a', newline='') as file:
                 writer = csv.writer(file)
                 writer.writerow(data_to_append)

      except Exception as e:
          #if any errors occur
          print(f"Error processing file {file_name}: {e}")
