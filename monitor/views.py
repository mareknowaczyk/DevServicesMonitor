from pyramid.view import view_config

class ProcessViews(object):
  def __init__(self, request):
    self.request = request 

  @view_config(route_name='list_json', renderer='json')
  def get_list_json( self ):
    return {}

  @view_config(route_name='index', renderer='monitor:templates/index.pt')
  def show_index(self):            

    return { }

