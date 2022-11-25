import numpy as np
import plotly.graph_objects as go
from enum import Enum, auto
from libs_tools.metrics.rowwise import rowwise_cosine

# TODO make_map sucks!
# TODO check if make_map modifies values
# TODO make_map transpose?
# TODO generalize id_from_index

class IndexType(Enum):
  """Class describing recognized types of measurement index -> 2d space mappings.
  """
  HORIZONTAL_SNAKE = auto()
  VERTICAL_SNAKE   = auto()
  HORIZONTAL       = auto()
  VERTICAL         = auto()


def id_from_index(x: int, y: int, dim: tuple[int, int], index: IndexType) -> int:
    """For given coordinates returns the index of corresponding spectra with respect to map 
    dimensions and index type.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            dim (tuple[int, int]): Map dimensions.

        Returns:
            int: Index of spectra. 
    """
    return y * dim[1] + (x if not y % 2 else dim[1] - x - 1)


def make_map(
    values: np.ndarray,
    dim: tuple[int, int],
    index_type: IndexType,
    inplace: bool=True
    ) -> np.ndarray:
    """Transforms 2d spectra matrix to 3d hyperspectral map.

        Args:
            values     (np.ndarray): 2d spectra matrix.
            dim        (tuple[int, int]): Map dimensions.
            index_type (IndexType): Defines the index -> 2d space mapping. See <IndexType> class.
            inplace    (bool): Whether to make a copy or modify the array given by <values>.
                Defaults to True.

        Returns:
            np.ndarray: 3d hyperspectral map
    """
    if not inplace:
        values = np.copy(values)
    if index_type in [IndexType.VERTICAL_SNAKE, IndexType.VERTICAL]:
        values = np.resize(values, dim[::-1]).transpose()
    else:
        values = np.resize(values, dim)

    if index_type == IndexType.HORIZONTAL_SNAKE:
        values[1::2, :] = values[1::2, ::-1]
    elif index_type == IndexType.VERTICAL_SNAKE:
        values[:, 1::2] = values[::-1, 1::2]

    return values


def plot_map(
    values: np.ndarray,                                                 
    dim: tuple[int, int],                                      
    index_type: IndexType=IndexType.HORIZONTAL_SNAKE,
    title: None | str=None,
    *args,
    **kwargs,                                                      
) -> go.Heatmap:
    """Plots a hyperspecral map. Args, kwargs are passed to go.Heatmap.

        Args:
            values     (np.ndarray): 2d spectra matrix.
            dim        (tuple[int, int]): Map dimensions.
            index_type (IndexType, optional): Defines the index -> 2d space mapping. See <IndexType> class.
            title      (None | str, optional): Figure title. Defaults to None.

        Returns:
            go.Heatmap: Hyperspecral map.
    """
    values = make_map(values, dim, index_type)

    fig = go.Figure(data=go.Heatmap(
        z=values,
        *args,
        **kwargs)
    )

    fig.update_layout(
        title=title,
    )

    return fig


def error_map(y_true: np.ndarray,                                             
              y_pred: np.ndarray,
              dim: tuple[int, int],                                            
              index_type: IndexType=IndexType.HORIZONTAL, 
              rowwise_error: callable[[np.ndarray, np.ndarray], np.array]=rowwise_cosine,                                          
              title: Optional[str]=None,                                                                                    
              add_stats: bool=False,
              *args,
              **kwargs                                         
              ):
  values = rowwise_error(y_true, y_pred)

  if add_stats:
    if not title:
      title = ''
    title += ' (avg: {}, min: {}, max: {})'.format(np.mean(values), np.min(values), np.max(values))

  return plot_map(values, dim, index_type, *args, **kwargs)


def intensity_map(spectra: np.array,
                  dim: Tuple[int, int],                                            
                  index_type: IndexType=IndexType.HORIZONTAL,                                  
                  start: Optional[T]=None,                                 
                  end: Optional[T]=None,                                   
                  calibration: Optional[Iterable[T]]=None,
                  *args,
                  **kwargs
                  ):
  values = spectra_intensity(spectra, start, end, calibration)

  return plot_map(values, dim, index_type, *args, **kwargs)


def spectra_intensity(spectra: np.array,                                     
                      start: Optional[T]=None,                                 
                      end: Optional[T]=None,                                   
                      calibration: Optional[Iterable[T]]=None,                 
                      ) -> Iterable[float]:
    if calibration is None:
      calibration = np.arange(spectra.shape[0])
    if start is None:
      start = calibration[0]
    if end is None:
      end = calibration[-1]

    return np.sum(LabelCropp(label_from=start, label_to=end, labels=calibration).fit_transform(spectra), axis=1)