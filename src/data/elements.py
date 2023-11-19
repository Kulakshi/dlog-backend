from src.models.elements import DataType, ElementType, Attribute

default_elements = [
    ElementType(
        name="TimeStamp",
        attributes=[],
        style={"color": "blue"},
        actions={},
    ),
    ElementType(
        name="Counter",
        attributes=[Attribute(name="step", type=DataType.number, value=1)],
        style={"color": "blue"},
        actions={},
    ),
    ElementType(
        name="Slider",
        attributes=[
            Attribute(name="min", type=DataType.number, value=0),
            Attribute(name="max", type=DataType.number, value=100),
            Attribute(name="label", type=DataType.text, value="Slider Label")
        ],
        style={"color": "blue"},
        actions={},
    ),
]