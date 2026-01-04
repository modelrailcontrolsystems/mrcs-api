"""
Created on 4 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)

https://realpython.com/command-line-interfaces-python-argparse/
"""

from mrcs_control.cli.args.control_args import ControlArgs


# --------------------------------------------------------------------------------------------------------------------

class TokenTimeoutArgs(ControlArgs):
    """unix command line handler"""

    def __init__(self, description):
        super().__init__(description)

        self._parser.add_argument('-s', '--set', action='store', type=int, nargs=2, help='set HOURS MINUTES')

        self._args = self._parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set(self):
        return bool(self._args.set)


    @property
    def hours(self):
        return self._args.set[0] if self.set else None


    @property
    def minutes(self):
        return self._args.set[1] if self.set else None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'TokenTimeoutArgs:{{set:{self._args.set}, indent:{self.indent}, verbose:{self.verbose}}}'
