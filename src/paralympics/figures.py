import pandas as pd
import plotly.express as px

from paralympics.models import Event, Participants


def line_chart(feature, db):
    """ Creates a line chart with data from paralympics_events.csv

     Parameters
     feature: events, sports, countries or participants

     Returns
     fig_html: Plotly Express line figure html/Javascript
     """

    # take the feature parameter from the function and check it is valid
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    else:
        # Make sure it is lowercase to match the dataframe column names
        feature = feature.lower()

    # Construct the query using FlaskSQLAlchemy.
    stmt = db.select(Event, Participants).join(Participants).order_by(Event.type, Event.year)

    # Create a dataframe from the Event objects using pd.read_sql_query()
    line_chart_df = pd.read_sql_query(stmt, db.get_engine())

    # Set the title for the chart using the value of 'feature'
    title_text = f"How has the number of {feature} changed over time?"

    '''
    Create a Plotly Express line chart with the following parameters
      line_chart_data is the DataFrane
      x="year" is the column to use as a x-axis
      y=feature is the column to use as the y-axis
      color="type" indicates if winter or summer
      title=title_text sets the title using the variable title_text
      labels={} sets the X label to Year, sets the Y axis and the legend to nothing (an empty string)
      template="simple_white" uses a Plotly theme to style the chart
    '''
    fig = px.line(line_chart_df,
                  x="year",
                  y=feature,
                  color="type",
                  title=title_text,
                  labels={'year': 'Year', feature: '', 'type': ''},
                  template="simple_white"
                  )

    # Convert to HTML
    fig_html = {"fig": fig.to_html(full_html=False, include_plotlyjs=True, div_id="line-chart")}
    return fig_html
