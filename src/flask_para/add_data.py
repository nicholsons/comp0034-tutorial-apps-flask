"""
Code from COMP0035
Contains functions to add data to the paralympics database.
Uses the SQLAlchemy object, db.
"""
from importlib import resources

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from flask_para import db
from flask_para.models import Country, Disability, DisabilityEvent, Event, Host, HostEvent, MedalResult, \
    Participants


def add_country_data(df):
    """Add the country data to the paralympics database."""
    # Insert all values into the country table
    try:
        for index, row in df.iterrows():
            # The row is pandas series, we want the series as a list of values
            row_values = row.tolist()
            new_country = Country(code=row_values[0],
                                  name=row_values[1],
                                  region=row_values[2],
                                  sub_region=row_values[3],
                                  member_type=row_values[4],
                                  notes=row_values[5])
            db.session.add(new_country)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f'An error occurred adding country data to the paralympics database. Error: {e}')
        db.session.rollback()  # Rollback the changes on error


def add_event_data(df):
    """Add event and participant data to the paralympics database."""
    try:
        # Convert the dates to strings
        df['start'] = df['start'].dt.strftime('%d/%m/%Y')
        df['end'] = df['end'].dt.strftime('%d/%m/%Y')

        # Insert the values into the event table
        for index, row in df.iterrows():
            event = Event(type=row['type'],
                          year=row['year'],
                          start=str(row['start']),
                          end=str(row['end']),
                          countries=row['countries'],
                          events=row['events'],
                          sports=row['sports'],
                          highlights=row['highlights'],
                          url=row['url'])

            # Use the relationship definition to add the participants data
            event.participants = Participants(participants_m=row['participants_m'],
                                              participants_f=row['participants_f'],
                                              participants=row['participants'])
            db.session.add(event)  # adds the events and participants data to the session
        db.session.commit()
    except SQLAlchemyError as e:
        print(f'An error occurred adding event data to the paralympics database. Error: {e}')
        db.session.rollback()


def add_host_data(df_events):
    """Add host data database."""

    try:
        # Extract unique host name and country pairs
        # Initialize an empty DataFrame with the columns needed
        host_country_df = pd.DataFrame(columns=['host', 'country'])
        # Iterate over each row in the events DataFrame and split each column into multiple values where there is ','
        for index, row in df_events.iterrows():
            hosts = row['host'].split(',')
            countries = row['country'].split(',')
            # Create pairs of each host with each country and append to the DataFrame
            for host, country in zip(hosts, countries):
                new_row = pd.DataFrame({'host': [host.strip()], 'country': [country.strip()]})
                host_country_df = pd.concat([host_country_df, new_row], ignore_index=True)
        # Remove duplicate hosts from the dataframe
        host_country_df = host_country_df.drop_duplicates(subset=['host', 'country'])

        # Iterate over the dataframe, add the host and country to the host table
        for index, row in host_country_df.iterrows():
            # Get the country code from the country table
            country_name = row['country']
            country = Country.query.filter_by(name=country_name).first()
            if country:
                new_host = Host(country_code=country.code, host=row['host'])
                db.session.add(new_host)
        # Commit the changes
        db.session.commit()

    except SQLAlchemyError as e:
        print(f'An error occurred adding host data to the paralympics database. Error: {e}')
        db.session.rollback()


def add_host_event_data(df):
    """Add HostEvent data to the paralympics database."""

    try:
        # Iterate each event, find the pairs of hosts, then get the event_id and host_id and insert into the host_event table
        for index, row in df.iterrows():
            hosts = row['host'].split(',')
            # Find the event id for the event. This matches based on the year and type of event.
            query = db.select(Event).where(Event.year == row['year'], Event.type == row['type'])
            event = db.session.execute(query).scalar_one_or_none()
            if event:
                event_id = event.event_id
                # Find the host_id for each host
                for host_name in hosts:
                    query = db.select(Host).where(Host.host == host_name.strip())
                    host = db.session.execute(query).scalar_one_or_none()
                    if host:
                        host_id = host.host_id
                        # Insert the host_event pair
                        new_host_event = HostEvent(host_id=host_id, event_id=event_id)
                        db.session.add(new_host_event)
        db.session.commit()

    except SQLAlchemyError as e:
        print(f'An error occurred adding host_event data to the paralympics database. Error: {e}')
        db.session.rollback()


def add_disabilities_data(df):
    """Add Disability and DisabilityEvent data."""

    try:
        # Split the comma-separated values into lists
        split_disabilities = df['disabilities'].str.split(', ')
        # Flatten the list of lists into a single list
        all_disabilities = [item for sublist in split_disabilities for item in sublist]
        # Convert the list to a set to get unique values
        unique_disabilities = set(all_disabilities)
        # Insert the unique values into the table
        for d in unique_disabilities:
            new_disability = Disability(category=d)
            db.session.add(new_disability)
        db.session.commit()

        # Iterate each result row in the event table
        for index, row in df.iterrows():
            # find the event
            query = db.select(Event).where(Event.year == row['year'], Event.type == row['type'])
            event = db.session.execute(query).scalar_one_or_none()
            if event:
                # Split the values for the disabilities
                disabilities = row['disabilities'].split(', ')
                # Add each disability
                for d in disabilities:
                    # Find the disability
                    query = db.select(Disability).where(Disability.category == d)
                    disability = db.session.execute(query).scalar_one_or_none()
                    if disability:
                        de = DisabilityEvent(event_id=event.event_id, disability_id=disability.disability_id)
                        event.disability_events.append(de)
                        disability.disability_events.append(de)
                db.session.commit()

    except SQLAlchemyError as e:
        print(f'An error occurred adding disability data to the paralympics database. Error: {e}')
        db.session.rollback()


def add_medal_result_data(df):
    """Add MedalResult data to the paralympics database."""
    try:
        # Iterate each result row, get the event_id and code and insert into the MedalResult table
        for index, row in df.iterrows():
            # Find the event id for the event. This matches based on the year and host name.
            query = db.select(Event).join(Event.host_events).join(HostEvent.host).where(Event.year == row['Year'], Host.host == row['Location'])
            event = db.session.execute(query).scalar_one_or_none()
            if event:
                # Insert the medal results
                event.medal_results.append(MedalResult(
                    country_code=row['NPC'],
                    rank=row['Rank'],
                    gold=row['Gold'],
                    silver=row['Silver'],
                    bronze=row['Bronze'],
                    total=row['Total']
                ))
                db.session.commit()

    except SQLAlchemyError as e:
        print(f'An error occurred adding MedalResult data. Error: {e}')
        db.session.rollback()


def add_all_data():
    """Adds all the data.
    """
    # Specifies the path to the data file
    data_path = resources.files("data").joinpath("paralympics.xlsx")

    # Read data and create pandas dataframes
    events_df = pd.read_excel(data_path, sheet_name='events')
    medals_df = pd.read_excel(data_path, sheet_name='medal_standings')
    npc_df = pd.read_excel(data_path, sheet_name='npc_codes')

    # List of tables and corresponding data addition functions
    tables_and_functions = [
        (Country, add_country_data, npc_df),
        (Event, add_event_data, events_df),
        (Host, add_host_data, events_df),
        (HostEvent, add_host_event_data, events_df),
        (Disability, add_disabilities_data, events_df),
        (MedalResult, add_medal_result_data, medals_df)
    ]

    # Iterate through each table and function
    for table, add_function, data in tables_and_functions:
        count_query = db.select(func.count()).select_from(table)
        if db.session.execute(count_query).scalar() == 0:
            add_function(data)
