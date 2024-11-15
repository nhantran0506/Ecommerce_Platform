"use client";
import CartItemCard from "@/components/cart_item_card";
import { ITableColumProp } from "@/interface/UI/ICartUI";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  getKeyValue,
  Button,
  Divider,
  Card,
  CardBody,
} from "@nextui-org/react";
import { ChevronLeft, X } from "react-feather";
import ProductNumberPicker from "@/components/product_number_picker";
import { productlist } from "@/data/data";

const CartPage = () => {
  const rows = productlist.map((product) => ({
    key: product.id,
    item: <CartItemCard product={product} onClick={() => {}} />,
    price: `$${product.price.toFixed(2)}`,
    quantity: <ProductNumberPicker />,
    total_price: `$${product.price.toFixed(2)}`,
  }));

  const columns: ITableColumProp[] = [
    {
      key: "item",
      label: "Item",
    },
    {
      key: "price",
      label: "Price",
    },
    {
      key: "quantity",
      label: "Quantity",
    },
    {
      key: "total_price",
      label: "Total Price",
    },
    {
      key: "options",
      label: "",
    },
  ];

  return (
    <div className="flex flex-col justify-center mx-64">
      <h1 className="font-bold text-xl mb-4 mt-12">
        Cart{" "}
        <span className="text-[#939699] font-normal">{productlist.length}</span>
      </h1>

      <Table aria-label="Cart table" className="mb-8">
        <TableHeader columns={columns}>
          {(column) => (
            <TableColumn key={column.key}>
              <p
                className={`text-sm ${
                  column.key === "quantity" ? "text-center" : ""
                }`}
              >
                {column.label}
              </p>
            </TableColumn>
          )}
        </TableHeader>
        <TableBody items={rows}>
          {(item) => (
            <TableRow key={item.key}>
              {(columnKey) => (
                <TableCell>
                  {columnKey === "options" ? (
                    <Button
                      variant="light"
                      color="danger"
                      isIconOnly
                      // onClick={() => handleDelete(item.key)}
                    >
                      <X />
                    </Button>
                  ) : (
                    getKeyValue(item, columnKey)
                  )}
                </TableCell>
              )}
            </TableRow>
          )}
        </TableBody>
      </Table>

      <Divider className="mb-8" />

      <div className="mb-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ChevronLeft size={18} className="text-[#BCBFC2]" />
          <p className="text-[#939699] font-bold">Back to shopping</p>
        </div>

        <div className="flex items-center gap-4">
          <p>
            Total Price: <span className="font-bold">$99.99</span>
          </p>

          <Button className="text-white bg-black rounded-full py-2 px-8 font-bold">
            Checkout
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
