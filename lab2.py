from spyre import server

import pandas as pd

class StockExample(server.App):
  title = "Inputs"

  inputs = [{   "type":'dropdown',
                "label": 'Index',
                "options" : [ {"label": "VCI", "value":"VCI"},
                                {"label": "TCI", "value":"TCI"},
                                {"label": "VHI", "value":"VHI"},],
                "key": 'index',
                "action_id": "update_data"},

              { "type":'dropdown',
                "label": 'Region',
                "options" : [ {"label": "Cherkasy", "value":"01"},
                                  {"label": "Chernihiv", "value":"02"},
                                  {"label": "Chernivtsi", "value":"03"},
                                  {"label": "Crimea", "value":"04"},
                                  {"label": "Dnipropetrovs'k", "value":"05"},
                                  {"label": "Donets'k", "value":"06"},
                                  {"label": "Ivano-Frankivs'k", "value":"07"},
                                  {"label": "Kharkiv", "value":"08"},
                                  {"label": "Kherson", "value":"09"},
                                  {"label": "Khmel'nyts'kyy", "value":"10"},
                                  {"label": "Kiev", "value":"11"},
                                  {"label": "Kiev City", "value":"12"},
                                  {"label": "Kirovohrad", "value":"13"},
                                  {"label": "Luhans'k", "value":"14"},
                                  {"label": "L'viv", "value":"15"},
                                  {"label": "Mykolayiv", "value":"16"},
                                  {"label": "Odessa", "value":"17"},
                                  {"label": "Poltava", "value":"18"},
                                  {"label": "Rivne", "value":"19"},
                                  {"label": "Sevastopol'", "value":"20"},
                                  {"label": "Sumy", "value":"21"},
                                  {"label": "Ternopil'", "value":"22"},
                                  {"label": "Transcarpathia", "value":"23"},
                                  {"label": "Vinnytsya", "value":"24"},
                                  {"label": "Volyn", "value":"25"},
                                  {"label": "Zaporizhzhya", "value":"26"},
                                  {"label": "Zhytomyr", "value":"27"}],
                "key": 'region',
                "action_id": "update_data"},

              { "input_type":"text",
                "variable_name":"year",
                "label": "Year",
                "value":1981,
                "key": 'year',
                "action_id":"update_data"},

              { "type":'slider',
                "label": 'First Week',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'first',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Last Week',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'last',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Area Percentage',
                "min" : 0,"max" : 100,"value" : 0,
                "key": 'percent',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'MIN VHI',
                "min" : 0,"max" : 100,"value" : 0,
                "key": 'minimum',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'MAX VHI',
                "min" : 0,"max" : 100,"value" : 100,
                "key": 'maximum',
                "action_id": 'update_data'},]

  controls = [{   "type" : "hidden",
                  "id" : "update_data"}]

  tabs = ["Graph", "Table", "Drought", "Extremum", "Size"]

  outputs = [{  "type" : "plot",
                "id" : "plot",
                "control_id" : "update_data",
                "tab" : "Graph"},
              { "type" : "table",
                "id" : "table",
                "control_id" : "update_data",
                "tab" : "Table"},
              { "type" : "html",
                "id" : "drought",
                "control_id" : "update_data",
                "tab" : "Drought"},
              { "type" : "table",
                "id" : "table1",
                "control_id" : "update_data",
                "tab" : "Extremum"},
              { "type" : "html",
                "id" : "data_size",
                "control_id" : "update_data",
                "tab" : "Size"}]

  def table(self, params):
    index = params['index']
    region = params['region']
    year = params['year']
    first = params['first']
    last = params['last']

    path = '2018_06_12-02h_vhi_id_{}.csv'.format(region)

    df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'provinceID', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    df1 = df[(df['year'] == float(year)) & (df['week'] >= float(first)) & (df['week'] <= float(last))]
    df1 = df1[['week', index]]
    return df1

  def getPlot(self, params):
    index = params['index']
    year = params['year']
    first = params['first']
    last = params['last']
    df = self.table(params).set_index('week')
    plt_obj = df.plot()
    plt_obj.set_ylabel(index)
    plt_obj.set_title('Index {index} for {year} from {first} to {last} weeks'.format(index=index,
      year=float(year), first=float(first), last=float(last)))
    fig = plt_obj.get_figure()
    return fig

  def drought(self, params):
    region = params['region']
    minimum = params['minimum']
    maximum = params['maximum']
    percent = params['percent']

    path = '2018_06_12-02h_vhi_id_{}.csv'.format(region)
    df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'provinceID', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    df1 = df[(df['VHI'] < int(maximum)) & (df['VHI'] > int(minimum))]
    df1 = df1[['year', 'VHI']]
    return 'Years with area percentage g.t. {percent} with drought: {years} years'.format(percent=int(percent),
      years = pd.unique(df1.year.ravel()))

  def table1(self, params):
      region = params['region']

      path = '2018_06_12-02h_vhi_id_{}.csv'.format(region)

      df = pd.read_csv(path, index_col=False, header=9,
                       names=['year', 'week', 'provinceID', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
      return df.loc[pd.concat((df.groupby(['year'])['VHI'].idxmax(), df.groupby(['year'])['VHI'].idxmin()))]

  def data_size(self, params):
      region = params['region']
      path = '2018_06_12-02h_vhi_id_{}.csv'.format(region)

      df = pd.read_csv(path, index_col=False, header=9,
                       names=['year', 'week', 'provinceID', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])

      return 'Dataframe size: {size}'.format(size=df.shape)


app = StockExample()
app.launch(port=8080)
