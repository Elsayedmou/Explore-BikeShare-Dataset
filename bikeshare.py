import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    DAY = {'sat': 'Saturday',
       'sun': 'Sunday',
       'mon': 'Monday',
       'tue': 'Tuesday',
       'wed': 'Wednesday',
       'thu': 'Thursday',
       'fri': 'Friday'}
    MONTH = {'jan': 'January',
         'feb': 'February',
         'mar': 'March',
         'apr': 'April',
         'may': 'May',
         'jun': 'June'}
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York, or Washington?\n').lower()
        if city not in CITY_DATA:
            print('\nInvalid City Name, Please try again!')
            continue
        else:
            break

    # Choose filter type by month only, day only or both. f_t refer to the filter type
    while True:
        filter_type = input('\nWould you like to filter data by Month, Day, Both, or Not at all? Type none for no time filter\n')
        if filter_type.lower() not in ('month', 'day', 'both', 'none'):
            print('\nInvalid City Name, Please try again!')
            continue
        #No filters
        elif filter_type.lower() == 'none':
            month = 'all'
            day = 'all'
            f_t = 'The data is not Filtered'
            break
        #Filter by Month
        elif filter_type.lower() == 'month':
            while True:
                month = input('\nWhich Month? Jan, Feb, Mar, Apr, May, or Jun?\n')
                if month.lower() not in MONTH:
                    print('Invalid Month, Please try again!')
                    continue
                else:
                    month = MONTH[month.lower()]
                    day = 'all'
                    f_t = 'The data is filtered by Month "{}"'.format(month)
                    break
            break
        #Filter by Day
        elif filter_type.lower() == 'day':
            while True:
                day = input('\nWhich Day? Sat, Sun, Mon, Tue, Wed, Thu, or Fri?\n')
                if day.lower() not in DAY:
                    print('Invalid day, Please try again!')
                    continue
                else:
                    month = 'all'
                    day = DAY[day.lower()]
                    f_t = 'The data is filtered by Day "{}"'.format(day)
                    break
            break
        #filter by both Month and Day
        elif filter_type.lower() == 'both':
            while True:
                month = input('\nWhich Month? Jan, Feb, Mar, Apr, May, or Jun?\n')
                if month.lower() not in MONTH:
                    print('Invalid Month, Please try again!')
                    continue
                else:
                    month = MONTH[month.lower()]
                    break
            while True:
                day = input('\nWhich Day? Sat, Sun, Mon, Tue, Wed, Thu, or Fri?\n')
                if day.lower() not in DAY:
                    print('Invalid day, Please try again!')
                    continue
                else:
                    day = DAY[day.lower()]
                    break
            f_t = 'The data is filtered by both Month "{}" & Day "{}"'.format(month,day)
            break
        
    print('-'*40)
    return city, month, day, f_t


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour_of_day'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mc_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    MCM = months[mc_month - 1]
    print('The most common month is : "{}" "{}"'.format(mc_month, MCM))

    # TO DO: display the most common day of week
    mc_day = df['day_of_week'].mode()[0]
    print('The most common day is : "{}"'.format(mc_day))

    # TO DO: display the most common start hour
    mc_hour = df['hour_of_day'].mode()[0]
    print('The most common hour is : "{}"'.format(mc_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    cm_st_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is : "{}"'.format(cm_st_station))

    # TO DO: display most commonly used end station
    cm_en_station = df['Start Station'].mode()[0]
    print('The most commonly used end station is : "{}"'.format(cm_en_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] =('from ' + df['Start Station'] + ' to ' + df['End Station'])
    cm_trip = df['Trip'].mode()[0]
    print('The most common trip is : "{}"'.format(cm_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    t_time = df['Trip Duration'].sum()
    print('The total travel time is : "{}" "Days"'.format(t_time/86400))
             
    # TO DO: display mean travel time
    avg_time = df['Trip Duration'].mean()
    print('The total travel time is : "{}" "Sec" "{}" "Min"'.format(avg_time,avg_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    num_users = df['User Type'].value_counts()
    print('Num. of different user is :\n{}\n'.format(num_users))
    
    # TO DO: Display counts of gender
    if city.lower() != 'washington':
        num_genders = df['Gender'].value_counts()
        print('Num. of different Genders is :\n{}\n'.format(num_genders))
    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_b = df['Birth Year'].min()
        print('Earliest birth of year is: "{}"\n'.format(earliest_b))
        most_recent_b = df['Birth Year'].max()
        print('Most recent birth of year is: "{}"\n'.format(most_recent_b))
        mc_birth = df['Birth Year'].mode()[0]        
        print('Most common birth of year is: "{}"\n'.format(mc_birth))
    else:
        print('\n###Washington dosen\'t have Genders Data###')        
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def disp_raw_data(df, f_t):
    """Display the first 5 raw data and the next 5 everytime the user type yes"""
    
    print('\nDisplaying Raw Data\n')
        
    #displaying the first 5 raws
    while True:
        first_raws =input('\nDo you want to see the first 5 lines of raw data? type yes, or no!\n')
        start_time = time.time()
        if first_raws.lower() == 'yes':
            print(df.head(5))
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40 + '\n' + f_t + '\n' + '-'*40)
            
            # Displaying the upcoming 5 raws 
            nxt = 0
            while True:
                disp_data =input('\nDo you want to see the next 5 lines ? type yes, or no!\n')
                if disp_data == 'yes':
                    st_time = time.time()
                    nxt += 5
                    print(df.iloc[nxt:nxt+5,:])
                    print("\nThis took %s seconds." % (time.time() - st_time))
                    print('-'*40 + '\n' + f_t + '\n' + '-'*40)
                    continue
                elif disp_data.lower() == 'no':
                    break
                else:
                    print('\nInvalid choise, Please try again!\n')
                    continue
            break
        elif first_raws.lower() == 'no':
            break
        else:
            print('\nInvalid choise, Please try again!\n')
            continue

def main():
    while True:
        city, month, day, f_t = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        print(f_t + '\n' + '-'*40)
        station_stats(df)
        print(f_t + '\n' + '-'*40)
        trip_duration_stats(df)
        print(f_t + '\n' + '-'*40)
        user_stats(df, city)
        print(f_t + '\n' + '-'*40)
        disp_raw_data(df, f_t)
                      

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
	main()
