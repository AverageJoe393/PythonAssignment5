'''
Name: Karl Honse
Date created: 11-13-2017
Purpose: turn a text file into a dictionary and organize the data 
'''
import pylab as py
import operator

def open_file():
    '''function used to open specified file that user enters'''
    while True:
        try:
            entry = input("Input a File name: ")
            file = open(entry, 'r') 
            break
        except FileNotFoundError: #if the file isn't found this error will occur 
            print("File not Found, Try again.")
    return file #returns a file pointer 
    
    
def update_dictionary(dictionary, year, hurricane_name, data):
    '''Function that gets used in the create_dictionary function in order to organize the data within the dictionary'''
    
    valueForYear = dictionary.get(year)

    
    if valueForYear == None:
        dictionary[year] = {}
        
    valueForYearName = dictionary[year].get(hurricane_name)
    if valueForYearName == None:
        dictionary[year][hurricane_name] = []
        
    if valueForYearName == None:
        dictionary[year][hurricane_name] = []
            
    dictionary[year][hurricane_name].append(data) #appends the data tuple to the dictionary   
    
    return dictionary #returns the formatted dictionary 
    

def create_dictionary():
    '''A function designed to see the data within the file specified from open_file then strip and split where needed to be able to organize the information'''
    file = open_file()
    D = {} #creating a blank dictionary
    
    key=operator.itemgetter(0,1) 
    for line in file:
        line = line.rstrip('\n') #for every line in the file strip away the new line character
        line = line.split(' ') #then split on every space
        
        year = line[0] #index 0 is the year
        hurricane_name = line[1] #index 1 is the name
        
        lat = float(line[3]) 
        long = float(line[4])
        date = line[5]
        
        try: #not all the wind levels are the same format, try yo make it a float, if unable just make it 0
            wind = float(line[6])
        except:
            wind = 0
        
        try: #same reasoning as the try statement for wind
            pressure = float(line[7])
        except:
            pressure = 0      
        
        data = (lat, long, date, wind, pressure) #the data tuple
        
        D = update_dictionary(D, year, hurricane_name, data) #call to update dictionary to put this now broken up data into the desired format in the dictionary
    return D #return the updated dictionary
            

def display_table(dictionary, year):
    '''Display the data in an easy to understand table rather than a big long string'''
    hurricanes = list(dictionary[year]) 
    hurricanes.sort()
    
    print('Peak Wind Speed for the Hurricanes in: %4s ' %year)
    
    print('\nNAME                Coordinates         WindSpeed(knots)     Date \n') #heading
    for name in hurricanes:
        record = dictionary[year][name]
        record.sort(reverse = True,key = operator.itemgetter(3,0,1)) #sorting the data first on wind then lat then long
        
        tup = record[0] 
        
        print('%-15s(%6.2f, %6.2f)%20.2f%16s' % (name, tup[0], tup[1], tup[3], tup[2])) #formatted line spacing for name, long, lat, wind speed and date
        

def get_years(dictionary):
    '''Gets the min and max years in the dictionary so the user knows the range of years that they can enter'''
    
    
    hurricanes = list(dictionary.keys()) #gets all the years from the dictionary
    hurricanes.sort() #sorts the years from smallest to largest
    #print(hurricanes)
    
    minYear = hurricanes[0] #the first year should be the smallest
    maxYear = hurricanes[-1] #the last year should be the largest
    
    #print(minYear, maxYear)
    return (minYear, maxYear) 
    

def prepare_plot(dictionary, year):
    '''Function that takes the dictionary and specified year and prepares the data that gets used in plot_wind_chart()'''
    names = list(dictionary[year].keys()) #gets all the names in the dictionary
    names.sort() #sorts the names alphabetically
    max_speed = [] #empty list for max_speed
    
    for hurricane in names: 
        record = dictionary[year][hurricane]
        tempMaxSpeed = record[0][3] #for each set of records in the hurricane names make the first one the max temporarily
        for each in record:
            if each[3] > tempMaxSpeed: #no go through all of them and if the next is bigger than the last make it the new temp max speed
                tempMaxSpeed = each[3]
        max_speed.append(tempMaxSpeed) #at the very end append the largest temp speed and that should be your max speed for that hurricane
        
    return (names, max_speed)


def plot_wind_chart(year,size,names,max_speed):
    '''Function that was already given to us, all we have to do is supply it with the year, number of names, the hurricane names and the max speeds'''
    
    # Set the value of the category
    cat_limit = [ [v for i in range(size)] for v in [64,83,96,113,137] ]
    
    
    # Colors for the category plots
    COLORS = ["g","b","y","m","r"]
    
    # Plot the Wind Speed of Hurricane
    for i in range(5):
        py.plot(range(size),cat_limit[i],COLORS[i],label="category-{:d}".format(i+1))
        
    # Set the legend for the categories
    py.legend(bbox_to_anchor=(1.05, 1.),loc=2,\
              borderaxespad=0., fontsize=10)
    
    py.xticks(range(size),names,rotation='vertical') # Set the x-axis to be the names
    py.ylim(0,180) # Set the limit of the wind speed
    
    # Set the axis labels and title
    py.ylabel("Wind Speed (knots)")
    py.xlabel("Hurricane Name")
    py.title("Max Hurricane Wind Speed for {}".format(year))
    py.plot(range(size),max_speed) # plot the wind speed plot
    py.show() # Show the plot


def main():
    '''Main function that calls the other functions in the order that this assignment requires it.'''
    
    dictionary = create_dictionary() #get the dictionary we're going to use throughout from create_dictionary()
    minYear = get_years(dictionary)[0] 
    maxYear = get_years(dictionary)[1]
    print('Hurricane Record Software Records from %4s to %4s\n' % (minYear, maxYear)) #used the return from get_years to help display the min and max years
    
        
    while True: 
        try: 
            yearEntry = str(input('Enter the year to show hurricane data or quit: ')) #while statement with nested if else in order for the user to be able to enter a year or quit the program
            if yearEntry == 'Q' or yearEntry == 'q' or yearEntry == 'Quit' or yearEntry == 'quit':
                print("\nProgram Execution Complete")
                break
            else:
                display_table(dictionary, yearEntry) #if they didn't quit sent the dictionary and yearEntry to the display_table function
            break
        except KeyError: #if anything entered in the yearEntry causes a KeyError give this prompt until a using input is entered 
            print('Enter a 4 digit year within the range of the record...')
    
    prepared = prepare_plot(dictionary, yearEntry) #gives the required variables to the prepare_plot function
    
    size = len(prepared[0]) #number of names in that given year
    names = prepared[0] #the names returned from prepare_plot
    max_speed = prepared[1] #the max speeds returned from prepare_plot
    #print(names)
    #print(max_speed)
    
    makeGraph = input ('Do you want to Plot? ') #input from the user required so the program knows whether or not to make the graph
    if makeGraph == 'yes' or makeGraph == 'Yes' or makeGraph == 'y' or makeGraph == 'Y': #if any form of yes is entered go through with sending the data to plot_wind_chart
        plot_wind_chart(int(yearEntry), size, names, max_speed)
    if makeGraph == 'no' or makeGraph == 'No' or makeGraph == 'n' or makeGraph == 'N': #if any form of no is entered end the program
        print("\nProgram Execution Complete")
    
   
   
    
if __name__ == "__main__":
    main()