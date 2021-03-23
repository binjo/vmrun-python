# pyvmrun
##Introduction

This is a python wrapper for vmrun, used to control VMWare virtual machines. It 
is based off of vmrun-python by @Binjo, whose idea is in-turn based on Alexander
Sotirov's vmrun-ruby. Assumed, same as original, to support only VMWare Fusion/WS
versions 6.0 and above.

## Basic Usage
```python
import pyvmrun
vm = pyvmrun.Vmrun( 'full/path/to/your/foo.vmx' )
vm.start()
vm.suspend()
vm.stop()
```

## Known Issues

1. Calls to revertToSnapshot may corrupt the VM's vmx file, causing the VM to 
   refuse to start. If this is the case, edit your vmx file:
   
   * remove the following line:
       
   ```bash
   checkpoint.vmState = "foo-SnapshotXX.vmsn"
   ```
   
   * edit vmx vmdk (disk) reference:
   ```bash
   # ide0:0.fileName = "foo-XXXXX.vmdk"
   # change to
   ide0:0.fileName = "foo.vmdk"
   ```

## Credits
Thanks to @Binjo and all original contributors for your work.