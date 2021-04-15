class CallsResultsHolder:
    date = None
    calls = None

    def __init__(self, date):
        self.date = date
        self.calls = []

    def add_call(self, the_call):
        self.calls.append(the_call)

    def get_date(self):
        return self.date

    def get_calls(self):
        return self.calls


class PutsResultsHolder:
    date = None
    puts = None

    def __init__(self, date):
        self.date = date
        self.puts = []

    def add_put(self, the_put):
        self.puts.append(the_put)

    def get_date(self):
        return self.date

    def get_puts(self):
        return self.puts
