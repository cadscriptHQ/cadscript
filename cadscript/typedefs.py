
from typing import Optional, Literal, Any, Optional, Union, Tuple

Vector2DType = Tuple[float, float]
Vector3DType = Tuple[float, float, float]
DimensionDefinitionType = Union[Vector2DType, float]
CenterDefinitionType = Union[Literal["X", "Y", "Z", "XY", "XZ", "YZ", "XYZ"], bool]
EdgeQueryType = str
FaceQueryType = str
AxisType = Literal["X", "Y", "Z"]
