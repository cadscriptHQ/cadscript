# Copyright (C) 2023-2024 Andreas Kahler
# This file is part of Cadscript
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, Union, Tuple

Vector2DType = Tuple[float, float]
Vector3DType = Tuple[float, float, float]
DimensionDefinitionType = Union[Vector2DType, float]
CenterDefinitionType = Union[Literal["X", "Y", "Z", "XY", "XZ", "YZ", "XYZ"], bool]
VertexQueryType = str
EdgeQueryType = str
FaceQueryType = str
AxisType = Literal["X", "Y", "Z"]
