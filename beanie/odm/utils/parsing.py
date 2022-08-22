from typing import Any, Type, Union, TYPE_CHECKING

from pydantic import BaseModel

from beanie.exceptions import (
    UnionHasNoRegisteredDocs,
    DocWasNotRegisteredInUnionClass,
)
from beanie.odm.interfaces.detector import ModelType

if TYPE_CHECKING:
    from beanie.odm.documents import Document


def parse_obj(
    model: Union[Type[BaseModel], Type["Document"]], data: Any
) -> BaseModel:
    if (
        not hasattr(model, "get_model_type")
        or model.get_model_type() != ModelType.UnionDoc
    ):
        # if hasattr(model, "_parse_obj_saving_state"):
        #     return model._parse_obj_saving_state(data)  # type: ignore
        return model.parse_obj(data)
    if model._document_models is None:
        raise UnionHasNoRegisteredDocs

    class_name = data["_class_id"] if isinstance(data, dict) else data._class_id
    if class_name not in model._document_models:
        raise DocWasNotRegisteredInUnionClass
    return parse_obj(model=model._document_models[class_name], data=data)
