import pandas as pd
import numpy as np
import time

# "welcome to this project about US bike share in different states "
print('Welcome to US bike share data analysis project.')

# First we need to put csv files (datasets) in a dictionary.

CITY_DATA_SETS =  { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


# Now we need some filters to work with.
# But we need to ask the users to give them.
def get_filters():
    print("let's choose a city to work with.")


    city = input('Would you like to see data for Chicago, New York, or Washington? ').lower()
    while city not in(CITY_DATA_SETS.keys()):
        print('You provided invalid city name')
        city = input('Would you like to see data for Chicago, New York, or Washington? ').lower()

# if city not in CITY_DATA_SETS.keys():
# print('not valid city,please try a different city'
# 'valid cities are Chicago, New york city and Washington')
# else:

# Get a filter from user filterizing the data by month, day or both.

    filter = input("Would you like your data sorted by month, day or both.").lower()
    while filter not in (['month', 'day', 'both']):
        print('not valid filter'
        '\nChoose between month, day and both')
        filter = input('Try again.')

    months = ['january', 'february', 'march', 'april', 'june']
    if filter == 'month' or filter == 'both':
        month = input("Which month would yo like to choose january, february, march, april or june ?").lower()
        while month not in months:
            print("Not valid month")
            month = input('Choose another month')

    else:
        month: str = 'all'

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if filter == 'day' or filter == 'both':
        day = input("Choose a day:").title()
        while day not in days:
            print("Not valid day")
#            "\nChoose another day.")
            day = input("choose another day:").title()
    else:
        day = 'all'
        print('_' * 50)
    return city, month, day


def lodaing_data(city, month, day):
    # loading data into a data frames.
    df = pd.read_csv(CITY_DATA_SETS[city])
    # changing date and time column to an object to ease dealing with.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # creating new columns for day of the week and the month.
    df['month'] = df['Start Time'].dt.month
    df['day_of_the_week'] = df['Start Time'].dt.day_name()


    if month != 'all':
        # using the index of months to get the corresponding number (int)
        months = ['january', 'february', 'march', 'april', 'june']
        month = months.index(month) + 1
        # filtering months to create a new dataframe
        df = df[df['month'] == month]
    if day != 'all':
        # using the index of days to get the corresponding number
     #   days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
     #   day = days.index(day) + 1
        df = df[df['day_of_the_week'] == day.title()]
    return df


def time_statistics(df):
    print("\n Calculating now the most common times(Month, Day or both) of travel...\n")
    start_time = time.time()
    # The most frequent time(month)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    print(f'The most common month is: {months[month-1]}')
    # The most frequent time(day)
    day = df['day_of_the_week'].mode()[0]
    print(f'The most common day of the week is:{day}')
    # Now we are going to calculate the most popular hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f'The most common hour is: {common_hour}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def station_statistics(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'The most popular start station is: {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'The most popular end station is: {common_end_station}')

    # display most frequent combination of start station and end station trip
    common_trip = df['Start Station'] + ' to ' + df['End Station']
    print(f'The most popular trip is: from {common_trip.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def trip_duration_statistics(df):
    from datetime import timedelta as td

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days = total_travel_duration.days
    hours = total_travel_duration.seconds // (60 * 60)
    minutes = total_travel_duration.seconds % (60 * 60) // 60
    seconds = total_travel_duration.seconds % (60 * 60) % 60
    print(f'Total travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds')

    # display mean travel time
    average_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days = average_travel_duration.days
    hours = average_travel_duration.seconds // (60 * 60)
    minutes = average_travel_duration.seconds % (60 * 60) // 60
    seconds = average_travel_duration.seconds % (60 * 60) % 60
    print(f'Average travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def user_statistics(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    print('\n\n')

    # Display counts of gender
    if 'Gender' in (df.columns):
        print(df['Gender'].value_counts())
        print('\n\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in (df.columns):
        year = df['Birth Year'].fillna(0).astype('int64')
        print(
            f'Earliest birth year is: {year.min()}\nmost recent is: {year.max()}\nand most comon birth year is: {year.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def display_raw_data(df):
    """Ask the user if he wants to display the raw data and print 5 rows at time"""
    raw = input('\nWould you like to diplay raw data?\n')
    if raw.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count + 5])
            count += 5
            ask = input('Next 5 raws?')
            if ask.lower() != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = lodaing_data(city, month, day)

        time_statistics(df)
        station_statistics(df)
        trip_duration_statistics(df)
        user_statistics(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


