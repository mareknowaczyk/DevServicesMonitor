# -*- coding: utf-8 -*-


from scripts.get_processes import (
    PowerShellCmdBuilder,
    parse_output,
    run_cmd,
    filter_cmd_output,
)

""" Abstract Command class """
class Command( object ):
    def __init__( self ):
        pass
    def execute( self ):
        raise Exception('Abstract method cannot be executed')

""" Command launcher """
class CmdCommand( Command ):
    def __init__( self, cmd ):
        self.cmd = cmd
        self._executor = run_cmd
    def execute( self ):
        return self._executor( self.cmd )


""" PowerShell command launcher """
class PowerShellCommand( CmdCommand ):
    def __init__( self, pscommand ):
        psb = PowerShellCmdBuilder()
        self.pscommand = pscommand
        self.cmd = psb.get_cmd( pscommand )
        self._executor = run_cmd

""" Listowanie procesów systemowych Windowsa wraz z filtrowaniem """
class GetProcessesCommand( PowerShellCommand ):
    def __init__( self, filters ):
        self.filters = filters
        psb = PowerShellCmdBuilder()
        self.fields = [ 'CommandLine',  'ProcessId', 'ProcessName', 'ExecutablePath' ]
        super(PowerShellCommand, self).__init__( psb.get_processes_cmd( self.fields ) )

    def execute( self ):
        res =parse_output( self.fields, super(PowerShellCommand, self).execute() )
        return filter_cmd_output( res, self.filters)        

if __name__ == "__main__":
    import sys
    out = GetProcessesCommand( [("CommandLine", sys.argv[1] ), ("ProcessName", 'pserve')] ).execute() 
    print "\n- - -\n".join( [ "\n".join([ "%s: %s" % (f,d[f]) for idx,f in enumerate(d) ]) for d in out ] )



