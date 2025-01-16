"""
Takes in a input of as list UTXOs and outputs of new UTXOs

used for normal transactions

"""

class Trx:

    def __init__(self, input, output):

        self.input = input
        self.output = output

    def _input_string(self):

        return [f"Input, {str(item)}" for item in self.input]


    def _output_string(self):

        return [f"Output, {str(item)}" for item in self.output]
        
    def __str__(self):
        
        return f"{self._input_string()}:{self._output_string()}"