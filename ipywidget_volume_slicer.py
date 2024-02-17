#!/usr/bin/env python
# coding: UTF-8


from typing import Optional

from IPython.display import display
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt


class VolumeSlicerWidget3D():
    def __init__(self, vol: npt.ArrayLike,
                 figsize=(6, 6),
                 repeat_z: Optional[int] = None,
                 cmap: str = 'jet',
                 vlim: Optional[list[int, int]] = None):
        # Parse arguments
        self.parse_args(vol, figsize, repeat_z, cmap, vlim)

        # Prepare widgets
        self.prepare_widgets()

        # Run widgets
        display(self.interactive1, self.interactive2)

    def parse_args(self, vol, figsize, repeat_z, cmap, vlim):
        self.vol = np.array(vol)
        self.vol_tmp = self.vol
        assert vol.ndim == 3
        nx, ny, nz = vol.shape

        self.figsize = figsize
        self.cmap = cmap

        if repeat_z is None:
            th_volume_xy_z_ratio = 5
            if (nx + ny)//2 > nz * th_volume_xy_z_ratio:
                self.repeat_z = 10
            else:
                self.repeat_z = 1

        if vlim is not None and hasattr(vlim, "__iter__"):
            self.v_min = vlim[0]
            self.v_max = vlim[1]
        else:
            self.v_min = np.min(vol)
            self.v_max = np.max(vol)

    def prepare_widgets(self):
        nx, ny, nz = self.vol.shape[:3]

        self.plane_dict = {
            'x-y': nz - 1,
            'y-z': nx - 1,
            'z-x': ny - 1,
        }
        self.orient = {"y-z": [2, 1, 0], "z-x": [2, 0, 1], "x-y": [0, 1, 2]}

        self.plane = widgets.ToggleButtons(
            options=self.plane_dict.keys(),
            value="x-y",
            description="Slice plane:",
            disabled=False
        )
        self.slider1 = widgets.IntSlider(min=0, max=nz-1, step=1,
                                         value=nz//2,
                                         description='Image Slice:')

        self.interactive1 = widgets.interactive(
            self.btn_handler, plane=self.plane)

        self.interactive2 = widgets.interactive(
            self.plot_slice, z=self.slider1)

        output = self.interactive2.children[-1]
        output.layout.height = f"{int(self.figsize[1]*90):d}px"

    def btn_handler(self, plane):
        if plane == "x-y":
            self.vol_tmp = self.vol
        else:
            self.vol_tmp = np.repeat(self.vol, self.repeat_z, axis=2)
            self.vol_tmp = np.transpose(self.vol_tmp, self.orient[plane])

        value_old = self.slider1.value
        value_new = self.plane_dict[plane] // 2
        max_old = self.slider1.max
        max_new = self.plane_dict[plane]

        if max_new < max_old:
            self.slider1.value = value_new
            self.slider1.max = max_new
        else:
            self.slider1.max = max_new
            if value_old == value_new:
                self.slider1.value = 0

            self.slider1.value = value_new

    def plot_slice(self, z):
        # Plot slice for the given plane and slice
        plt.figure(2, figsize=self.figsize)
        plt.axes().set_aspect('equal', 'datalim')
        plt.imshow(self.vol_tmp[:, :, z], cmap=plt.get_cmap(self.cmap),
                   vmin=self.v_min, vmax=self.v_max)
        plt.colorbar()


class VolumeSlicerWidget4D(VolumeSlicerWidget3D):
    def prepare_widgets(self):
        super().prepare_widgets()

        nx, ny, nz, na = self.vol.shape[:4]

        # Override properties
        self.orient = {"y-z": [2, 1, 0, 3],
                       "z-x": [2, 0, 1, 3], "x-y": [0, 1, 2, 3]}
        self.slider2 = widgets.IntSlider(min=0, max=na-1, step=1,
                                         value=na//2,
                                         description='4th Dimension:')
        self.interactive2 = widgets.interactive(
            self.plot_slice, z=self.slider1, a=self.slider2)

    def plot_slice(self, z, a):
        # Plot slice for the given plane and slice
        plt.figure(figsize=self.figsize)
        plt.axes().set_aspect('equal', 'datalim')
        plt.imshow(self.vol_tmp[:, :, z, a], cmap=plt.get_cmap(self.cmap),
                   vmin=self.v_min, vmax=self.v_max)
        plt.colorbar()


class VolumeSlicerWidget5D(VolumeSlicerWidget3D):
    def prepare_widgets(self):
        super().prepare_widgets()

        nx, ny, nz, na, nb = self.vol.shape[:5]

        # Override properties
        self.orient = {"y-z": [2, 1, 0, 3, 4],
                       "z-x": [2, 0, 1, 3, 4],
                       "x-y": [0, 1, 2, 3, 4]}
        self.slider2 = widgets.IntSlider(min=0, max=na-1, step=1,
                                         value=na//2,
                                         description='4th Dimension:')
        self.slider3 = widgets.IntSlider(min=0, max=nb-1, step=1,
                                         value=nb//2,
                                         description='5th Dimension:')
        self.interactive2 = widgets.interactive(
            self.plot_slice, z=self.slider1, a=self.slider2, b=self.slider3)

    def plot_slice(self, z, a, b):
        # Plot slice for the given plane and slice
        plt.figure(figsize=self.figsize)
        plt.axes().set_aspect('equal', 'datalim')
        plt.imshow(self.vol_tmp[:, :, z, a, b], cmap=plt.get_cmap(self.cmap),
                   vmin=self.v_min, vmax=self.v_max)
        plt.colorbar()
