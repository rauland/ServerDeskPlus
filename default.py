from dataclasses import dataclass, field
# TODO use dataclass
# TODO change default.py into search.py, moving query from getrequests into this module

# Default object parms for SD query
class Parms :
  def __init__(self, start_index = 1, row_count = 100, day = 1, month = 0,choice = "open",fields_required='[get_all]'):
    self.start_index = start_index
    self.row_count = row_count
    self.day = day
    self.month = month
    self.choice = choice
    self.fields_required = fields_required

  @dataclass
  class Search:
    start_index: int = 1
    row_count: int = 100
    day: int = 1
    month: int = 0
    choice: str = "open"
