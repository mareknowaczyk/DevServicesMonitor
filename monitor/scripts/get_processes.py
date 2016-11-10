
#/c/Windows/system32/WindowsPowerShell/v1.0/powershell "Get-WmiObject Win32_Process | Format-List -Property CommandLine"
#(Get-Process -id 5060).StartInfo.EnvironmentVariables

import subprocess
import re

class PowerShellCmdBuilder:
    def __init__(self):
        self.ps_cmd = r"c:\Windows\system32\WindowsPowerShell\v1.0\powershell"
        self.cmds = {
                    'ps' : self.ps_cmd,
                    'processes' : "Get-WmiObject Win32_Process",
                    'format-list' : 'Format-List -Property ',
                    'get-process-env' : '(Get-Process -id %s).StartInfo.EnvironmentVariables'
                }
    def get_cmd(self, win_cmd_line):
        return '%s "%s"' % (
                self.cmds['ps'],
                win_cmd_line,
        )

    def get_partial_pipe_cmd(self, partial_cmds):
        return " | ".join( partial_cmds )

    def get_partial_mapped_cmd(self, mapped_cmd, args):
        if not (mapped_cmd in self.cmds):
            return ""

        return self.cmds[ mapped_cmd ] % args
        
    def get_processes_cmd(self, columns=["CommandLine", "id"], grep_args=""):
        return '%s "%s | %s %s %s"' % ( 
                self.cmds['ps'],
                self.cmds['processes'],
                self.cmds['format-list'] ,
                ",".join(columns),
                ( " | grep %s " % grep_args )if grep_args else " " 
        )

def parse_output(fields, output ):
    res = []
    idx = 0;    
    last_field = ""
    last_field_start = -1
    lines = output.split("\r\n")
    obj = None
    for line in lines:        
        if line.strip() == "":
            continue
        idx = -1
        for f in fields:
            idx = line.find( f )
            if idx == 0:                
                if ( (not obj) or (f in obj) ):
                    obj = dict()
                    res.append( obj )
                last_field_start = line.find( ': ')+2
                obj[f] = line[ last_field_start: ]
                last_field = f
                break
        
        if (idx <> 0) and ((last_field_start > 0) and (last_field)):
            obj[last_field] = obj[last_field] + line[ last_field_start: ]
    return res

def run_cmd( cmd ):
    defsGroup = {}
    defs = {}    
    pr = subprocess.Popen( cmd , shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
    (out, error) = pr.communicate()
    if (error):
        raise Exception("run_cmd: ", error)
        exit
    return out

"""
filter_cmd_output( output, filters)
    - output is formatted cmd output
    - filters is collections of tuples:
        ( field, regex), where
        - field is key of output values
        - regex - regular expression of filter
"""
def filter_cmd_output( output, filters ):    
    res = []
    filters = filters[:]
    filters = [ (field, regex, 1 ) for field, regex in filters ]

    for item in output:
        is_found = []
        for idx, tup in enumerate(filters):
            field, regex, dirtyflag = tup            
            if dirtyflag and (field in item):                
                if re.search( regex, item[field]):
                    is_found.append(1)
                    continue
            else:
                filters[idx] = (field, regex, 0)
        if (len(is_found) == len( filters )):
            res.append( item )

    return res


if __name__ == "__main__":
    fields = [ 'CommandLine',  'ProcessId', 'ProcessName', 'ExecutablePath' ]
    spb = PowerShellCmdBuilder()
    cmd = spb.get_processes_cmd( fields )
    out = run_cmd( cmd )
    res = parse_output( fields, out )

    #    print "\n".join( [ "-"*80+"\n"+ "\n".join( [ "%s : %s" % (k, p[k]) for k in p  ] ) for p in res if p['CommandLine'].find('pserve')>=0 ] )

    print "\n------------------\n".join( [ "ProcessName: %s\nProcessId: %s\nExecutablePath: %s\nCommandLine: %s\n" % (
        p['ProcessName'],
        p['ProcessId'],
        p['ExecutablePath'],
        p['CommandLine']
        ) for p in res if p['CommandLine'].find('pserve')>=0] )

    #print [ p for p in res if p['CommandLine'].find('pserve')>=0] 
    #print res

    ids = [ p['ProcessId'] for p in res if p['CommandLine'].find('pserve')>=0 ]

    import re

    for id in ids:
        break
        print id
        cmd = spb.get_cmd( spb.get_partial_mapped_cmd( 'get-process-env', id) )
        print cmd
        print re.search("pwd",  run_cmd( cmd )).groups()


    print (run_cmd( spb.get_cmd( "Get-Process | Get-Member" )  ))
    #print (run_cmd( spb.get_cmd( "Get-Process | Select-Object Path" )  ))



