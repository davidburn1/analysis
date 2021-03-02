# Code for the analysis of soft x-ray synchrotron experiments

This repository contains a selection of codes to aid with the analysis of data collected for soft x-ray experiments on the I10 beamline at Diamond Light Source synchrotron.

The experiments include:
- x-ray magnetic circular dichroism (XMCD)
- x-ray detected ferromagnetic resonance (XFMR)
- resonant elastic x-ray scattering (REXS)

Publications based on data analysed with these codes can be found in my [publication list](https://davidburn1.github.io/publications). 


# X-ray Magnetic Circular Dichroism (XMCD)

When the energy on circularly polarized x-rays matches the element specific x-ray absorption edge of a ferromagnetic material, a peak in the absorption is detected. There is a difference in the absorption at these edges due to both the polarization of the x-rays and the projection of the magnetization onto the beam direction.

By scanning the x-ray energy over the abrosption edges, the absorption spectra in two states with either opposite magnetization or measured with opposite polarization can be compared. The energy at which the differnce between the absorption spectra is maximised, is the optimal energy for performing element specific magnetization studies.

The code here is used to analyse multiple energy scans, interpolating them onto the same energy axis, and plotting the absorption spectra along with the difference. The maximum difference is also extracted.

# X-ray detected FerroMagnetic Resonance (XFMR)

The magnetization orientation within a magnetic material will precess when excited by an RF magnetic field. The resonance frequency, at which this effect is maximized, follows a Kittel curve shape on a frequency-field map which is commonly measured using vector-network-analyser ferromagnetic resonance.

The time-dependent and element specific information can be extracted from the resonance using XFMR. Here, the XMCD signal is measured stroboscopically whilst the dynamics in the sample are excited with a RF source which is phase locked to integer multiples of the synchrotron master clock.

The projection of the magnetization is measured as a function of a variable delay introduced between the RF pump and x-ray probe. The signal follows a sinusoidal shape and this code fits these sin waves for each scan measured in different field. The amplitude and phase of the dynamic signal are extracted for comparison with a typical ferromagnetic resonance crossing involving a Lorentzian peak in the amplitude accompanied with a 180 degree shift in phase.

# Resonant Elastic X-ray Scattering (REXS)

In REXS experiments, the magnetic ordering in a sample is probed in an x-ray scattering geometry. Ordered magnetic structures give rise to additional scattering peaks in addition to structural scattering peaks. REXS measurements are commonly used to explore the phase diagrams of topologically rich chiral magnetic materials to identify phases such as helical, conical and skyrmion ordering. 

The codes here are useful for converting the images collected on an x-ray sensitive CCD camera into peak locations in reciprocol space. They also help with the visualization of the data through the construction of movies, and arrangement of the data into phase diagrams.



# Usage

To download a copy of the code:
    git clone https://github.com/davidburn1/analysis.git

To upload any changes:
    git add .
    git commit -m "message"
    git push -f origin master

To download any changes:
    git pull



git remote add upstream https://github.com/davidburn1/analysis.git
git fetch upstream (sync local with the upstream)
git merge upstream/master   (perform the merge)



