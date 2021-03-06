import os
import sys
import subprocess
import string
import shutil
from pathlib import Path
from CellModeller.Simulator import Simulator
import numpy as np

n_steps = 400

def simulate(modfilename, platform, device, steps=50):
    (path,name) = os.path.split(modfilename)
    modname = str(name).split('.')[0]
    print('Loading ', modname)
    sys.path.append('.')
    sim = Simulator(modname, 0.5, clPlatformNum=platform, clDeviceNum=device, saveOutput=True)
    for t in range(n_steps):
        sim.step()
    del(sim)

def main():
    # Get module name to load
    if len(sys.argv)<2:
        print("Please template model (.py) file")
        exit(0)
    else:
        template = open(sys.argv[1], 'rt').read()

    # Get OpenCL platform/device numbers
    if len(sys.argv)<3:
        # User input of OpenCL setup
        import pyopencl as cl
        # Platform
        platforms = cl.get_platforms()
        print("Select OpenCL platform:")
        for i in range(len(platforms)):
            print(('press '+str(i)+' for '+str(platforms[i])))
        platnum = int(eval(input('Platform Number: ')))

        # Device
        devices = platforms[platnum].get_devices()
        print("Select OpenCL device:")
        for i in range(len(devices)):
            print(('press '+str(i)+' for '+str(devices[i])))
        devnum = int(eval(input('Device Number: ')))
    else:
        platnum = int(sys.argv[2])
        devnum = int(sys.argv[3])

    N = 1000
    for Wc in np.linspace(0, 0.5, 10):
        for psi in np.linspace(0, 1, 10):
            for ftax in [0]:
                model = template%(N, Wc, psi, ftax)
                outfn = 'Wc__%g__psi__%g__ftax__%g__%d_cells'%(Wc, psi, ftax, N)
                outfn = outfn.replace('.', '_') + '.py'
                print('Creating model file %s'%outfn)
                outf = open(outfn, 'wt')
                outf.write(model)
                outf.close()
                # Set up complete, now run the simulation
                simulate(outfn, platnum, devnum)
                os.remove(outfn)

# Make sure we are running as a script
if __name__ == "__main__": 
    main()
