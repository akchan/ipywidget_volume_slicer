# ipywidget_volume_slicer

An image viewer widget for volume data (3D, 4D, 5D)

## Features

- Simple image viewer for volume data
- Works on jupyter notebook even on visual code studio
- Interactive viewing

## Screenshot

![screenshot](./screenshot.png)

## Usage

```py
from ipywidget_volume_slicer import VolumeSlicerWidget3D

# Read your volume data
vol = read_volume_data()

VolumeSlicerWidget3D(vol)
```

## How to run the example

```bash
git clone https://github.com/akchan/ipywidget_volume_slicer.git

jupyter-notebook ipywidget_volume_slicer/example.ipynb
```

## License

MIT License
