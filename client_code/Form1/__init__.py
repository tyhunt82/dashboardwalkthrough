from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from datetime import datetime

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    self.temp_data = []
    self.build_revenue_graph()
    self.build_signups_graph()
    self.build_marketing_graph()
    self.build_weather_graph()
     
  def build_revenue_graph(self):
    # self.plot_1.data = go.Bar(y=[100,400,200,300,500])
    db_data = anvil.server.call('get_revenue')
    self.plot_1.data = go.Bar(x = [x['date'] for x in db_data],
                              y = [x['amount'] for x in db_data],
                              marker=dict(color='#2196f3'))
    self.style_plot(self.plot_1)
    self.plot_1.layout.title = "REVENUE GROWTH"
    max_revenue = sorted(db_data, key=lambda x: x['amount'], reverse=True)[0]
    self.revenue_label.text = "{}, {:,}".format(max_revenue['date'].strftime("%d %b %Y"), max_revenue['amount'])
    
  def build_signups_graph(self):
    signups = anvil.server.call('get_user_signups')
    scatter = go.Scatter(x = [x['date'] for x in signups],
                         y = [x['signups'] for x in signups],
                         fill = 'tozeroy',
                         line=dict(color='#2196f3'))
    self.plot_2.data = scatter
    self.style_plot(self.plot_2)
    self.plot_2.layout.title = "USER SIGNUPS"
    max_signups = sorted(signups, key=lambda x: x['signups'], reverse=True)[0]
    self.signups_label.text = "%s, %d" % (max_signups['date'].strftime("%d %b %Y"), max_signups['signups'])

     
  def build_marketing_graph(self):
    marketing_data = anvil.server.call('get_marketing_data')
    self.plot_3.data = go.Scatter(x = [x['strategy'] for x in marketing_data],
                               y = [x['count'] for x in marketing_data],
                              mode='lines+markers',
                              line=dict(color='#2196f3'))
    self.style_plot(self.plot_3)
    self.plot_3.layout.title = "HITS BY MARKETING STRATEGY"
    max_hits = sorted(marketing_data, key=lambda x: x['count'], reverse=True)[0]
    self.marketing_label.text = "%s, %d hits" % (max_hits['strategy'], max_hits['count'])
        
  def build_weather_graph(self):
    # Retrieve data from api. We'll use latitude and longitude for Cambridge for this example.
    weather_data = anvil.server.call('get_weather_data', 52.2053, 0.1218)
    # Add time and temperature data from api to our temp_data variable.
    self.temp_data.append({'time':weather_data['time'], 'temp':weather_data['temp']})
    self.style_plot(self.plot_4)
    self.plot_4.layout.title = "REAL-TIME TEMPERATURE DATA: CAMBRIDGE"
    self.plot_4.layout.yaxis.title = "Temperature, Fahrenheit"
    self.plot_4.data = go.Scatter(y=[x['temp'] for x in self.temp_data], 
                                  x=[x['time'] for x in self.temp_data], 
                                  line=dict(color='#2196f3'))
    
    max_temp = sorted(self.temp_data, key=lambda x: x['temp'], reverse=True)[0]
    self.weather_label.text = "%.1f" % max_temp['temp']
    
  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    with anvil.server.no_loading_indicator:
      self.build_weather_graph()
    
  def style_plot(self, plot):
    # expand the graphs
    plot.layout = go.Layout(
        margin=dict(
            l=50, #left margin
            r=50, #right margin
            b=50, #bottom margin
            t=50, #top margin
        ),
        font=dict(family='Arial', size=10),
        xaxis=dict(
          zeroline=False,
          tickfont=dict(
              family='Arial',
              size=11,
              color='#808080'
          ),
        ),
        yaxis=dict(
            zeroline=False,
            tickfont=dict(
                family='Arial',
                size=11,
                color='#808080'
            ),
        ))

  
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    isVisible = self.column_panel_1.visible
    if isVisible:
      self.column_panel_1.visible = False
    else:
      self.column_panel_1.visible = True








