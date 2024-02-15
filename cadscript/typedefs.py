# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, Union, Tuple

Vector2DType = Tuple[float, float]
Vector3DType = Tuple[float, float, float]
DimensionDefinitionType = Union[Tuple[float, float], float]
CenterDefinitionType = Union[Literal["X", "Y", "Z", "XY", "XZ", "YZ", "XYZ"], bool]
CenterDefinition2DType = Union[Literal["X", "Y", "XY"], bool]
AxisType = Literal["X", "Y", "Z"]
Axis2DType = Literal["X", "Y"]
