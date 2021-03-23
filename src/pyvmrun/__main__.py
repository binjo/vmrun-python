#!/usr/bin/env python
"""
Platform-independent VMWare/vmrun control from Python

@author : bpengu1n <bpengu1n@penguin-sec.org>
@date   : 2021/03/23
"""

__description__ = "Platform-independent VMWare/vmrun control from Python"
__author__      = "bpengu1n"
__version__     = "0.2.0"
__date__        = "2021/03/23"
__license__     = "GNU GPL v3+"

#
# Forked from vmrun- v0.1.4, @binjo <binjo.cn@gmail.com>
# Based on vmrun-ruby, Alexander Sotirov <asotirov@determina.com>
#
import os
import subprocess
import sys


class Vmrun(object):

    def execute( self, path, *cmd ):

        cmds   = list(cmd)
        cmds.insert( 1, "\"%s\"" % self.VM_FILE )
        cmds[0] = "-T %s -gu %s -gp %s %s" % (self.VM_PRODUCT, self.VM_ADMIN, self.VM_PASS, cmds[0])
        params = " ".join( cmds )

        if self.DEBUG: print("[DEBUG] %s" % params)

        if sys.platform == "win32":
            cmd = "%s %s" % (path, params)
        else:
            cmd = ["sh", "-c", "%s %s" % (path, params)]

        p = subprocess.Popen( cmd, stdout=subprocess.PIPE )

        return p.stdout.readlines()

    def vmrun(self, *cmd):
        return [_.decode('utf-8') for _ in self.execute( self.VMRUN_PATH, *cmd )]

    # TODO maintain vm's power state
    def __init__( self, vmx, user='', password='', vmrun='', debug=False, product='ws' ):

        self.VM_FILE    =   vmx         # TODO strict censor?
        self.VM_PRODUCT =   product     # 'ws', 'server' or 'fusion' 
        self.VM_ADMIN   =   user
        self.VM_PASS    =   password
        self.DEBUG      =   debug

        if vmrun != '':
            self.VMRUN_PATH = vmrun
        else:
            if sys.platform == "win32":
                # get vmrun.exe's full path via registry
                import winreg
                reg = winreg.ConnectRegistry( None, winreg.HKEY_LOCAL_MACHINE )
                try:
                    rh = winreg.OpenKey( reg, r'SOFTWARE\VMware, Inc.\VMware Workstation' )
                    try:
                        vw_dir = winreg.QueryValueEx( rh, 'InstallPath' )[0]
                    finally:
                        winreg.CloseKey( rh )
                finally:
                    reg.Close()

                if vw_dir != '':
                    self.VMRUN_PATH = vw_dir + 'vmrun.exe'
            else:
                if "PATH" in os.environ:
                    for path in os.environ["PATH"].split(os.pathsep):
                        tmp_file = path + os.sep + "vmrun"
                        if os.path.exists(tmp_file):
                            self.VMRUN_PATH = tmp_file
                            break
                    # escape spaces in path
                    self.VMRUN_PATH = self.VMRUN_PATH.replace(' ', '\\ ')

    #
    # POWER COMMANDS
    #
    def start( self ):
        """
        COMMAND                  PARAMETERS           DESCRIPTION
        start                    Path to vmx file     Start a VM or Team
                                 or vmtm file
        """
        return self.vmrun( 'start' )

    def stop( self, mode='soft' ):
        """
        stop                     Path to vmx file     Stop a VM or Team
                                 or vmtm file
                                 [hard|soft]
        """
        return self.vmrun( 'stop', mode )

    def reset( self, mode='soft' ):
        """
        reset                    Path to vmx file     Reset a VM or Team
                                 or vmtm file
                                 [hard|soft]
        """
        return self.vmrun( 'reset', mode )

    def suspend( self, mode='soft' ):
        """
        suspend                  Path to vmx file     Suspend a VM or Team
                                 or vmtm file
                                 [hard|soft]
        """
        return self.vmrun( 'suspend', mode )

    def pause( self ):
        """
        pause                    Path to vmx file     Pause a VM
        """
        return self.vmrun( 'pause' )

    def unpause( self ):
        """
        unpause                  Path to vmx file     Unpause a VM
        """
        return self.vmrun( 'unpause' )

    #
    # SNAPSHOT COMMANDS
    #
    def listSnapshots( self ):
        return self.vmrun( 'listSnapshots' )

    def snapshot( self, name ):
        """
        snapshot                 Path to vmx file     Create a snapshot of a VM
                                 Snapshot name
        """
        return self.vmrun( 'snapshot', name )

    def deleteSnapshot( self, name ):
        """
        deleteSnapshot           Path to vmx file     Remove a snapshot from a VM
                                 Snapshot name
        """
        return self.vmrun( 'deleteSnapshot', name )

    def revertToSnapshot( self, name ):
        """
        revertToSnapshot         Path to vmx file     Set VM state to a snapshot
                                 Snapshot name
        """
        return self.vmrun( 'revertToSnapshot', name )

    #
    # RECORD/REPLAY COMMANDS
    #
    def beginRecording( self, snap_name ):
        """
        beginRecording           Path to vmx file     Begin recording a VM
                                 Snapshot name
        """
        return self.vmrun( 'beginRecording', snap_name )

    def endRecording( self ):
        """
        endRecording             Path to vmx file     End recording a VM
        """
        return self.vmrun( 'endRecording' )

    def beginReplay( self, snap_name ):
        """
        beginReplay              Path to vmx file     Begin replaying a VM
                                 Snapshot name
        """
        return self.vmrun( 'beginReplay', snap_name )

    def endReplay( self ):
        """
        endReplay                Path to vmx file     End replaying a VM
        """
        return self.vmrun( 'endReplay' )

    #
    # GUEST OS COMMANDS
    #
    def runProgramInGuest( self, program, mode, *para ):
        """
        runProgramInGuest        Path to vmx file     Run a program in Guest OS
                                 [-noWait]
                                 [-activeWindow]
                                 [-interactive]
                                 Complete-Path-To-Program
                                 [Program arguments]
        """
        modes = { "n" : "-noWait",
                  "a" : "-activeWindow",
                  "i" : "-interactive" }

        if mode in modes:
            return self.vmrun( 'runProgramInGuest', modes[mode], program, *para )
        else:
            return "error mode : %s" % mode

    # return True/False
    def fileExistsInGuest( self, file ):
        """
        fileExistsInGuest        Path to vmx file     Check if a file exists in Guest OS
                                 Path to file in guest
        """

        return "not" not in "".join( self.vmrun( 'fileExistsInGuest', file ) )

    def setSharedFolderState( self, share_name, new_path, mode='readonly' ):
        """
        setSharedFolderState     Path to vmx file     Modify a Host-Guest shared folder
                                 Share name
                                 Host path
                                 writable | readonly
        """
        return self.vmrun( 'setSharedFolderState', share_name, new_path, mode )

    def addSharedFolder( self, share_name, host_path ):
        """
        addSharedFolder          Path to vmx file     Add a Host-Guest shared folder
                                 Share name
                                 New host path
        """
        return self.vmrun( 'addSharedFolder', share_name, host_path )

    def removeSharedFolder( self, share_name ):
        """
        removeSharedFolder       Path to vmx file     Remove a Host-Guest shared folder
                                 Share name
        """
        return self.vmrun( 'removeSharedFolder', share_name )

    def enableSharedFolders( self ):
        """
        enableSharedFolders      Path to vmx file     Enable shared folders in Guest
                                 [runtime]
        """
        return self.vmrun( 'enableSharedFolders' )

    def disableSharedFolders( self ):
        """
        disableSharedFolders     Path to vmx file     Disable shared folders in Guest
                                 [runtime]
        """
        return self.vmrun( 'disableSharedFolders' )

    def listProcessesInGuest( self ):
        """
        listProcessesInGuest     Path to vmx file     List running processes in Guest OS
        """
        return self.vmrun( 'listProcessesInGuest' )

    def killProcessInGuest( self, pid ):
        """
        killProcessInGuest       Path to vmx file     Kill a process in Guest OS
                                 process id
        """
        return self.vmrun( 'killProcessInGuest', pid )

    def runScriptInGuest( self, interpreter_path, script ):
        """
        runScriptInGuest         Path to vmx file     Run a script in Guest OS
                                 Interpreter path
                                 script_text
        """
        return self.vmrun( 'runScriptInGuest', interpreter_path, script )

    def deleteFileInGuest( self, file ):
        """
        deleteFileInGuest        Path to vmx file     Delete a file in Guest OS
                                 Path in guest
        """
        return self.vmrun( 'deleteFileInGuest', file )

    def createDirectoryInGuest(self, dirname):
        """
        createDirectoryInGuest   Path to vmx file     Create a directory in Guest OS
                                 Directory path in guest
        """
        return self.vmrun( 'createDirectoryInGuest', dirname)

    def deleteDirectoryInGuest(self, dirname):
        """
        deleteDirectoryInGuest   Path to vmx file     Delete a directory in Guest OS
                                 Directory path in guest
        """
        return self.vmrun( 'deleteDirectoryInGuest', dirname)

    def listDirectoryInGuest(self, dirname):
        """
        listDirectoryInGuest     Path to vmx file     List a directory in Guest OS
                                 Directory path in guest
        """
        return self.vmrun( 'listDirectoryInGuest', dirname)

    def copyFileFromHostToGuest( self, host_path, guest_path ):
        """
        copyFileFromHostToGuest  Path to vmx file     Copy a file from host OS to guest OS
                                 Path on host
                                 Path in guest
        """
        return self.vmrun( 'copyFileFromHostToGuest', host_path, guest_path )

    def copyFileFromGuestToHost( self, guest_path, host_path ):
        """
        copyFileFromGuestToHost  Path to vmx file     Copy a file from guest OS to host OS
                                 Path in guest
                                 Path on host
        """
        return self.vmrun( 'copyFileFromGuestToHost', guest_path, host_path )

    def renameFileInGuest( self, org_name, new_name ):
        """
        renameFileInGuest        Path to vmx file     Rename a file in Guest OS
                                 Original name
                                 New name
        """
        return self.vmrun( 'renameFileInGuest', org_name, new_name )

    def captureScreen( self, path_on_host ):
        """
        captureScreen            Path to vmx file     Capture the screen of the VM to a local file
                                 Path on host
        """
        return self.vmrun( 'captureScreen', path_on_host )

    def writeVariable( self, mode, v_name, v_value ):
        """
        writeVariable            Path to vmx file     Write a variable in the VM state
                                 [runtimeConfig|guestEnv]
                                 variable name
                                 variable value
        """
        if mode is not None:
            return self.vmrun( 'writeVariable', mode, v_name, v_value )
        else:
            return self.vmrun( 'writeVariable', v_name, v_value )

    def readVariable( self, mode, v_name ):
        """
        readVariable             Path to vmx file     Read a variable in the VM state
                                 [runtimeConfig|guestEnv]
                                 variable name
        """
        if mode is not None:
            return self.vmrun( 'readVariable', mode, v_name )
        else:
            return self.vmrun( 'readVariable', v_name )

    #
    # VPROBE COMMANDS
    #
    def vprobeVersion( self ):
        """
        vprobeVersion            Path to vmx file     List VP version
        """
        return self.vmrun( 'vprobeVersion' )

    def vprobeLoad( self, script ):
        """
        vprobeLoad               Path to vmx file     Load VP script
                                 'VP script text'
        """
        return self.vmrun( 'vprobeLoad', script )

    def vprobeLoadFile( self, vp ):
        """
        vprobeLoadFile           Path to vmx file     Load VP file
                                 Path to VP file
        """
        return self.vmrun( 'vprobeLoadFile', vp )

    def vprobeReset( self ):
        """
        vprobeReset              Path to vmx file     Disable all vprobes
        """
        return self.vmrun( 'vprobeReset' )

    def vprobeListProbes( self ):
        """
        vprobeListProbes         Path to vmx file     List probes
        """
        return self.vmrun( 'vprobeListProbes' )

    def vprobeListGlobals( self ):
        """
        vprobeListGlobals        Path to vmx file     List global variables
        """
        return self.vmrun( 'vprobeListGlobals' )

    #
    # GENERAL COMMANDS
    #
    def list( self ):
        """
        list                                          List all running VMs
        """
        return self.vmrun( 'list' )

    def upgradevm( self ):
        """
        upgradevm                Path to vmx file     Upgrade VM file format, virtual hw
        """
        return self.vmrun( 'upgradevm' )

    def installtools( self ):
        """
        installtools             Path to vmx file     Install Tools in Guest OS
        """
        return self.vmrun( 'installtools' )

    def register( self ):
        """
        register                 Path to vmx file     Register a VM
        """
        return self.vmrun( 'register' )

    def unregister( self ):
        """
        unregister                 Path to vmx file     Unregister a VM
        """
        return self.vmrun( 'unregister' )

    def listRegisteredVM( self ):
        """
        listRegisteredVM                              List registered VMs
        """
        return self.vmrun( 'listRegisteredVM' )

    def deleteVM( self ):
        """
        deleteVM                 Path to vmx file     Delete a VM
        """
        return self.vmrun( 'deleteVM' )

    def clone( self, dest_vmx, mode, snap_name ):
        """
        clone                    Path to vmx file     Create a copy of the VM
                                 Path to destination vmx file
                                 full|linked
                                 [Snapshot name]
        """
        return self.vmrun( 'clone', dest_vmx, mode, snap_name )


if __name__ == '__main__':
    print('Hello World')
