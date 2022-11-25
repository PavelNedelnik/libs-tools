import numpy as np
import plotly.graph_objects as go
from libs_tools.metrics.rowwise import rowwise_euclid
from libs_tools.visualization.hyperspectral.utils import IndexType, plot_map
from libs_tools.preprocessing import LabelCropp

# TODO typing TypeVars?


def error_map(y_true: np.ndarray,                                             
              y_pred: np.ndarray,
              dim: tuple[int, int],                                            
              index_type: IndexType=IndexType.HORIZONTAL_SNAKE, 
              rowwise_error: callable[[np.ndarray, np.ndarray], np.array]=rowwise_euclid,                                          
              title: None | str=None,                                                                                    
              add_stats: bool=False,
              *args,
              **kwargs                                         
              ) -> go.Heatmap:
    """Calculate and plot the model error to a hyperspectral map. Args, kwargs are passed to the 
    <plot_map> function.

        Args:
            y_true (np.ndarray): Model output.
            y_pred (np.ndarray): Expected output.
            dim (tuple[int, int]): Map dimensions.
            index_type (IndexType, optional): Defines the index -> 2d space mapping. See <IndexType>
                class. Defaults to IndexType.HORIZONTAL_SNAKE.
            rowwise_error (callable[[np.ndarray, np.ndarray], np.array], optional): Error function 
                to apply to each spectra pair. Defaults to rowwise_euclid.
            title (None | str, optional): Figure title. Defaults to None.
            add_stats (bool, optional): Whether to add basic statistics of the error function to the
                 figure title. Defaults to False.

        Returns:
            go.Heatmap: Model error plotted to a hyperspectral map.
    """
    values = rowwise_error(y_true, y_pred)

    if add_stats:
        if not title:
            title = ''
        title += ' (avg: {}, min: {}, max: {})'.format(values.mean(), values.min(), values.max())

    return plot_map(values, dim, index_type, *args, **kwargs)


def intensity_map(
    spectra: np.ndarray,
    dim: tuple[int, int],
    calibration: None | np.array=None,                                          
    index_type: IndexType=IndexType.HORIZONTAL_SNAKE,                                  
    start: None | float=None,                                 
    end: None | float=None,                                   
    *args,
    **kwargs
    ) -> go.Heatmap:
    """Calculate and plot total intensity over a given range to a hyperspectral map. Args, kwargs
    are passed to the <plot_map> function.

        Args:
            spectra (np.ndarray): 2d spectra matrix.
            dim (tuple[int, int]): Map dimensions.
            calibration (None | np.array, optional): Measured wavelengths. Defaults to None.
            index_type (IndexType, optional): Defines the index -> 2d space mapping. See <IndexType>
                class. Defaults to IndexType.HORIZONTAL_SNAKE.
            start (None | float, optional): First wavelength to sum. Defaults to None.
            end (None | float, optional): Last wavelength to sum. Defaults to None.

        Returns:
            go.Heatmap: Spectra intensity plotted to a hyperspectral map.
    """
    if calibration is None:
      calibration = np.arange(spectra.shape[0])
    if start is None:
      start = calibration[0]
    if end is None:
      end = calibration[-1]

    values = np.sum(
        LabelCropp(label_from=start, label_to=end, labels=calibration).fit_transform(spectra),
        axis=1
    )

    return plot_map(values, dim, index_type, *args, **kwargs)