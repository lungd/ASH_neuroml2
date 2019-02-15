import sys
import os
from pyneuroml import pynml
from c302 import c302_utils

#import matplotlib
#matplotlib.rcParams['mathtext.fontset'] = 'cm'
#matplotlib.rc('font', family='serif', serif='CMU Serif')
import matplotlib.pyplot as plt

import signal


def create_plots(lems_file, simulator, directory, save, save_image_full_dir, show_plot_already, plot_ca, plot_connectivity, verbose):
    if simulator == 'jNeuroML':
        results = pynml.run_lems_with_jneuroml(lems_file, nogui=True, load_saved_data=True, verbose=verbose)
    elif simulator == 'jNeuroML_NEURON':
        results = pynml.run_lems_with_jneuroml_neuron(lems_file, nogui=True, load_saved_data=True, verbose=verbose)
        
    print("Finished simulation of %s and have reloaded results"%lems_file)

    #print results

    out = {}
    t = []
    for key, value in results.items():
        if key == 't':
            t = value
        else:
            label = key.split('/')[-1]
            print label
            if label == 'v':
                out[label] = [float(i) * 1e3 for i in value]
            elif label == 'S':
                out[label] = [float(i) * 1e-3 for i in value]
            else:
                out[label] = [float(i) * 1e6 for i in value]


    i = 33330
    print out['S'][i]
    print out['J_SERCA'][i]

    Ca = out['caConc']
    Rmin=min(Ca);
    Rmax=max(Ca);
    Rmin=4.963093110035229
    Rmax=32.282101799695049
    print Rmin
    print Rmax
    R0 = Rmax * Ca[0]**(1.7) / (Ca[0]**(1.7) + 2.5**(1.7)) / 100*(Rmax-Rmin)+Rmin
    #R=Rmax*Ca.^1.7./(Ca.^1.7+2.5^1.7)/100*(Rmax-Rmin)+Rmin;

    FRET = []
    for c in Ca:
        R = Rmax * c**(1.7) / (c**(1.7) + 2.5**(1.7)) / 100*(Rmax-Rmin)+Rmin;
        #R = 5
        y=(R-R0)/R0*100;
        FRET.append(y)


    fig = plt.figure()
    fig.set_size_inches(12, 8)

    fluxes = fig.add_subplot(221)
    voltage = fig.add_subplot(222)
    concentration = fig.add_subplot(223)
    fret = fig.add_subplot(224)

        

    fluxes.plot(t, out['J_PMCA'], label='J_PMCA', color='royalblue', linestyle='-')
    fluxes.plot(t, out['J_SERCA'], label='J_SERCA', color='chocolate', linestyle='--')
    fluxes.plot(t, out['J_TRPV'], label='J_TRPV', color='#F0BE4B', linestyle='-.')
    fluxes.plot(t, out['J_IPR'], label='J_IPR', color='darkviolet', linestyle=':')
    #fluxes.plot(t, out['J_VGCC'], label='J_VGCC', linestyle='-', marker='o')
    fluxes.plot(t, out['J_VGCC'], label='J_VGCC', color='limegreen', linestyle='-')
    fluxes.plot(t, out['J_LeakER'], label='J_LeakER', color='silver', linestyle='-')
    fluxes.plot(t, out['S'], label='Stimulus', color='red', linestyle='-', linewidth=0.6)
    fluxes.legend(loc='upper left', frameon=False, prop={'size': 6})
    fluxes.set_xlim([0, 55])
    fluxes.set_ylim([-0.3, 6])  
    fluxes.set_xlabel("Time (s)")
    fluxes.set_ylabel("[Ca2+ flux] (%sM/s)" % u'\u03bc')

    voltage.plot(t, out['v'], label="v")
    voltage.set_xlim([0, 55])
    voltage.set_ylim([-70, 20])    
    voltage.set_ylabel('Voltage (mV)')
    voltage.set_xlabel("Time (s)")

    concentration.plot(t, out['caConc'], label="caConc")
    concentration.set_xlim([0, 55])
    concentration.set_ylim([0, 0.5])
    concentration.set_ylabel('[Ca2+] (%sM)' % u'\u03bc')
    concentration.set_xlabel("Time (s)")

    concER = concentration.twinx()
    concER.plot(t, out['concentrationER'], color='grey', linewidth=0.5)
    concER.set_ylim([0, 300])
    concER.set_ylabel('[Ca2+]ER (%sM)' % u'\u03bc', color='grey')
    concER.tick_params('y', colors='grey')


    fret.plot(t, FRET, label="FRET")
    fret.set_xlim([0, 55])
    fret.set_ylim([-1, 10])
    fret.set_ylabel('FRET ratio change (%)')
    fret.set_xlabel("Time (s)")

    plt.subplots_adjust(wspace=0.4)

    plt.show()


def main():
    lems_file = 'LEMS_ASH_Stim.xml'
        
    #simulator = 'jNeuroML_NEURON'
    simulator = 'jNeuroML'
    directory = '.'
    save = False
    save_image_full_dir='.'
    show_plot_already = True
    plot_ca = False
    plot_connectivity = False
    verbose = True

    try:
        create_plots(lems_file, simulator, directory, save, save_image_full_dir, show_plot_already, plot_ca, plot_connectivity, verbose)
    except KeyboardInterrupt:
        print "quit"
        # quit
        plt.close()
        sys.exit()


if __name__ == '__main__':
    main()


