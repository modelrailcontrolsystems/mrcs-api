"""
Created on 30 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

https://realpython.com/command-line-interfaces-python-argparse/
"""

from mrcs_core.cli.args.mrcs_args import MRCSArgs


# --------------------------------------------------------------------------------------------------------------------

class UvicornArgs(MRCSArgs):
    """unix command line handler"""

    def __init__(self, description):
        super().__init__(description)

        self._parser.add_argument('-r', '--reload', action='store_true', help='reload on changed source')

        self._args = self._parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def reload(self):
        return self._args.reload


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'UvicornArgs:{{test:{self.test}, reload:{self.reload}, indent:{self.indent}, verbose:{self.verbose}}}'
