import numpy as np
import plotly.graph_objects as go
import colorlover as cl

# TODO single spectrum support
# TODO better args, kwargs
# TODO colormap docs

def plot_spectra(
    spectra: np.ndarray,
    calibration: None | np.array=None,
    title: None | str=None,
    labels: None | list[str]=None,
    colormap: None | list=cl.scales['12']['qual']['Paired'],
    axis_titles: bool=True,
    *args,
    **kwargs,
    ) -> go.Figure:
    """Creates a line plot with a single line for each spectrum. Args, kwargs are passed to 
    go.Scatter.

        Args:
            spectra     (np.ndarray): 2d array. Each row corresponds to a single spectrum.
            calibration (None | np.array, optional): Measured wavelengths. Defaults to None.
            title       (None | str, optional): Figure title. Defaults to None.
            labels      (None | list[str], optional): Labels for each spectrum. Defaults to None.
            colormap    (None | list, optional): Colormap. Defaults to cl.scales['12']['qual']['Paired'].
            axis_titles (bool, optional): Whether to auto generate axis titles. To generate titles 
                manually, use the <go.Figure.update_layout> method.

        Returns:
            go.Figure: Line plot of given spectra."""
    if calibration is None:
        calibration = np.arange(len(spectra[0]))
    if labels is None:
        labels = ["class {}".format(x+1) for x in range(len(spectra))]
    fig = go.Figure()
    for i in range(len(spectra)):
        fig.add_trace(
            go.Scatter(
                x = calibration,
                y = spectra[i],
                name = str(labels[i]),
                line = {'color': colormap[i % len(colormap)]},
                *args,
                **kwargs
            )
        )
    fig.update_layout(
        title = title,
        xaxis_title = "wavelength (nm)" if axis_titles else "",
        yaxis_title = "intensity (a.u.)" if axis_titles else "",
    )
    return fig