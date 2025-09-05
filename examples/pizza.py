from enum import auto
from typing import Annotated, List

from bytex import Structure, StructureEnum
from bytex.endianness import Endianness
from bytex.length_encodings import Prefix, Terminator
from bytex.types import U8, U16


class OrderType(StructureEnum(U8)):  # type: ignore[misc]
    DINE_IN = auto()
    DELIVERY = auto()
    PICKUP = auto()


class Topping(Structure):
    name: Annotated[str, Terminator("\0")]


class Pizza(Structure):
    pizza_id: U16
    toppings: Annotated[List[Topping], Prefix(U8)]


class PizzaOrder(Structure):
    order_type: OrderType
    customer_id: U16
    pizzas: Annotated[List[Pizza], Prefix(U8)]


def main() -> None:
    order = PizzaOrder(
        order_type=OrderType.DELIVERY,
        customer_id=1234,
        pizzas=[
            Pizza(pizza_id=1, toppings=[Topping(name="Onions")]),
            Pizza(
                pizza_id=2,
                toppings=[Topping(name="Extra Cheese"), Topping(name="Mushrooms")],
            ),
        ],
    )

    print(order)

    print(f"Order Dumped: {order.dump(endianness=Endianness.BIG)!r}")

    roundtrip = PizzaOrder.parse(order.dump())

    assert roundtrip.pizzas[0].toppings[0].name == "Onions"


if __name__ == "__main__":
    main()
