                                                            _    _
                                                           | |  | |
__   __ _ __ ___   _ __  _   _  _ __  ______  _ __   _   _ | |_ | |__    ___   _ __
\ \ / /| '_ ` _ \ | '__|| | | || '_ \|______|| '_ \ | | | || __|| '_ \  / _ \ | '_ \
 \ V / | | | | | || |   | |_| || | | |       | |_) || |_| || |_ | | | || (_) || | | |
  \_/  |_| |_| |_||_|    \__,_||_| |_|       | .__/  \__, | \__||_| |_| \___/ |_| |_|
                                             | |      __/ |
                                             |_|     |___/

                                                                            (*) 0.1.4

-*0 Intro 0*-

This is a python wrapper of vmrun.exe, which is used to control Vmware. Its idea is
based on Alexander Sotirov's vmrun-ruby. Currently it only support vmware 6.0 or
higher version.

-*0 Usage 0*-

import vmrun
vm = vmrun.Vmrun( r'full\path\to\your\foo.vmx', 'username', 'pass' )
vm.start()
vm.suspend()
vm.stop()

More fun refer to the source :-)

-*0 Known issue 0*-

1. When call revertToSnapshot, it may mess the vmware's vmx file, the Vmware may refuse
   to start. If this is the case, edit your vmx file, remove the following line:
       checkpoint.vmState = "foo-SnapshotXX.vmsn"
   edit vmx file:
       ide0:0.fileName = "foo-XXXXX.vmdk"
   to the original disk file
       ide0:0.fileName = "foo.vmdk"

-*0 Greetingz 0*-

Dedicate this to my dear Sierra.
Many thx to xIkUg/RCT, and all members of RCT, www.debugman.com.

                                                                     _________________
                                                                    /    Binjo/RCT    \
                                                                  /____ 2008.04.02______\
