# !/usr/bin/env python

import datetime
import os
import pathlib

# Import libraries
import betfairlightweight
import pandas as pd

# Change this certs path to wherever you're storing your certificates
certs_path = os.path.join(pathlib.Path(__file__).parent.absolute(), "certs")

# Change these login details to your own
my_username = "dahuuhad"
my_password = "A6ThczpbHkGTS8E"
my_app_key = "FV0tliCXuM87WIbR"

trading = betfairlightweight.APIClient(username=my_username,
                                       password=my_password,
                                       app_key=my_app_key,
                                       certs=certs_path,
                                       locale="sweden")

trading.login()

# Grab all event type ids. This will return a list which we will iterate over to print out the id and the name of the sport

sport_filter = betfairlightweight.filters.market_filter(
    text_query="Soccer"
    )

event_types = trading.betting.list_event_types(
    filter=sport_filter
)

sport_ids = pd.DataFrame({
    'Sport': [event_type_object.event_type.name for event_type_object in event_types],
    'ID': [event_type_object.event_type.id for event_type_object in event_types]
}).set_index('Sport').sort_index()

print(sport_ids['ID'].unique())

# Get a datetime object in a week and convert to string
datetime_in_a_week = (datetime.datetime.utcnow() + datetime.timedelta(weeks=1)).strftime("%Y-%m-%dT%TZ")
datetime_in_a_day = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%TZ")

# Create a competition filter
competition_filter = betfairlightweight.filters.market_filter(
    event_type_ids=list(sport_ids['ID'].unique()), # Soccer's event type id is 1
    market_start_time={
        'to': datetime_in_a_day
    },
    market_type_codes=['MATCH_ODDS']
)
print(competition_filter)

# Get a list of competitions for soccer
competitions = trading.betting.list_competitions(
    filter=competition_filter
)

# Iterate over the competitions and create a dataframe of competitions and competition ids
soccer_competitions = pd.DataFrame({
    'Competition': [competition_object.competition.name for competition_object in competitions],
    'ID': [competition_object.competition.id for competition_object in competitions]
})
# Get the English Premier League Competition ID
print(soccer_competitions[soccer_competitions.Competition.str.contains('')])

soccer_events = trading.betting.list_events(
    filter = competition_filter
)

# Create a DataFrame with all the events by iterating over each event object
soccer_events_weekly = pd.DataFrame({
    'Event Name': [event_object.event.name for event_object in soccer_events],
    'Event ID': [event_object.event.id for event_object in soccer_events],
    'Event Venue': [event_object.event.venue for event_object in soccer_events],
    'Country Code': [event_object.event.country_code for event_object in soccer_events],
    'Time Zone': [event_object.event.time_zone for event_object in soccer_events],
    'Open Date': [event_object.event.open_date for event_object in soccer_events],
    'Market Count': [event_object.market_count for event_object in soccer_events]
})

print(soccer_events_weekly)
#print(soccer_events_weekly['Event ID'].unique())
# Define a market filter
market_types_filter = betfairlightweight.filters.market_filter(
    event_type_ids=list(sport_ids['ID'].unique()), # Soccer's event type id is 1
 #   market_start_time={
 #       'to': datetime_in_a_day
 #       },
    market_type_codes=['OVER_UNDER_25']
)

# Request market types
market_types = trading.betting.list_market_types(
        filter=market_types_filter
)

# Create a DataFrame of market types
market_types_soccer = pd.DataFrame({
    'Market Type': [market_type_object.market_type for market_type_object in market_types],
})

market_catalogue_filter = betfairlightweight.filters.market_filter(
    event_ids=['30185023']
)

market_catalogues = trading.betting.list_market_catalogue(
    filter=market_types_filter,
    max_results='10',
    sort='FIRST_TO_START',
    market_projection=['RUNNER_DESCRIPTION', 'EVENT'],
    lightweight=False
)
#print(market_catalogues)
# Create a DataFrame for each market catalogue
market_types_mooney_valley = pd.DataFrame({
    'Event ID': [market_cat_object.event.id for market_cat_object in market_catalogues],
    'Event Name': [market_cat_object.event.name for market_cat_object in market_catalogues],
    'Market Name': [market_cat_object.market_name for market_cat_object in market_catalogues],
    'Market ID': [market_cat_object.market_id for market_cat_object in market_catalogues],
    'Total Matched': [market_cat_object.total_matched for market_cat_object in market_catalogues],
})

print(market_types_mooney_valley.to_string())

def process_runner_books(runner_books):
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''
    best_back_prices = [runner_book.ex.available_to_back[0].price
                        if runner_book.ex.available_to_back[0].price
                        else 1.01
                        for runner_book
                        in runner_books]
    best_back_sizes = [runner_book.ex.available_to_back[0].size
                       if runner_book.ex.available_to_back[0].size
                       else 1.01
                       for runner_book
                       in runner_books]

    best_lay_prices = [runner_book.ex.available_to_lay[0].price
                       if runner_book.ex.available_to_lay[0].price
                       else 1000.0
                       for runner_book
                       in runner_books]
    best_lay_sizes = [runner_book.ex.available_to_lay[0].size
                      if runner_book.ex.available_to_lay[0].size
                      else 1.01
                      for runner_book
                      in runner_books]

    selection_ids = [runner_book.selection_id for runner_book in runner_books]
    last_prices_traded = [runner_book.last_price_traded for runner_book in runner_books]
    total_matched = [runner_book.total_matched for runner_book in runner_books]
    statuses = [runner_book.status for runner_book in runner_books]
    scratching_datetimes = [runner_book.removal_date for runner_book in runner_books]
    adjustment_factors = [runner_book.adjustment_factor for runner_book in runner_books]

    df = pd.DataFrame({
        'Selection ID': selection_ids,
        'Best Back Price': best_back_prices,
        'Best Back Size': best_back_sizes,
        'Best Lay Price': best_lay_prices,
        'Best Lay Size': best_lay_sizes,
        'Last Price Traded': last_prices_traded,
        'Total Matched': total_matched,
        'Status': statuses,
        'Removal Date': scratching_datetimes,
        'Adjustment Factor': adjustment_factors
    })
    return df

# Create a price filter. Get all traded and offer data
price_filter = betfairlightweight.filters.price_projection(
    price_data=['EX_BEST_OFFERS']
)
for market_id in market_types_mooney_valley['Market ID']:
    # Request market books
    market_books = trading.betting.list_market_book(
        market_ids=[market_id],
        price_projection=price_filter,
        currency_code='SEK'
    )

    # Grab the first market book from the returned list as we only requested one market
    market_book = market_books[0]
    print(market_types_mooney_valley)
    runners_df = process_runner_books(market_book.runners)

    print(runners_df.to_markdown())