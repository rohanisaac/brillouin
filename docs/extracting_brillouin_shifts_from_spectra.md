EXTRACTING BRILLOUIN SHIFTS FROM SPECTRA

The spectrum contains three elastic peaks which I call L1, L2 and L3. They usually fall at approximately channels L1=5, L2=127, and L3=254 (out of 256). The spectrum also contains four inelastic peaks which can fall anywhere else, but channels P1=60, P2=70, P3=185 and P4=197 might be typical.

The mirror spacing is d, given in centimeters. d=0.56 cm is typical. Note that this is the “notional” spacing, approximately 0.2 cm larger than the “nominal” spacing read off the dial on the instrument. (It’s hard to calibrate this exactly, since you can’t bring the mirrors to zero spacing, i.e. touching, without damaging them.) The free spectral range, given in cm<sup>-1</sup>, is FSR = 1/(2d) = 0.89 cm<sup>-1</sup> for the values given here.

The wavenumber/channel is calculated by noting that the (average of the) spacing between elastic peaks is equal to the FSR. Thus [(L2 - L1) + (L3 - L2)]/2 = (L3 – L1)/2 = FSR.

This calibrates the wavenumber/channel: wn/ch = 2\*FSR/(L3 – L1) = 1/[d(L3 – L1)] = 0.00717 cm<sup>-1</sup>/ch for these values.

If the peaks are not crossed, then the frequency shifts are calculated thus:

> f<sub>1</sub> = (P1 – L1)(wn/ch) = 0.395 cm<sup>-1</sup>
>
> f<sub>2</sub> = (L2 – P2)(wn/ch) = 0.409 cm<sup>-1</sup>
>
> f<sub>3</sub> = (P3 – L2)(wn/ch) = 0.416 cm<sup>-1</sup>
>
> f<sub>4</sub> = (L3 – P4)(wn/ch) = 0.409 cm<sup>-1</sup>
>
> The relevant number is the average of these four, i.e. f = 0.407 cm<sup>-1</sup> with the uncertainty calculated using the normal methods.

If the peaks are crossed, then the frequency shifts are calculated thus:

> f<sub>1</sub> = (P2 – L1)(wn/ch) = 0.466 cm<sup>-1</sup>
>
> f<sub>2</sub> = (L2 – P1)(wn/ch) = 0.481 cm<sup>-1</sup>
>
> f<sub>3</sub> = (P4 – L2)(wn/ch) = 0.502 cm<sup>-1</sup>
>
> f<sub>4</sub> = (L3 – P3)(wn/ch) = 0.495 cm<sup>-1</sup>
>
> The relevant number is the average of these four, i.e. f = 0.486 cm<sup>-1</sup> with the uncertainty calculated using the normal methods.

The spectrum gives no indication if it is crossed or not, this must be decided using additional information. The variation among frequency values for the four peaks will typically be smaller than is given here.
