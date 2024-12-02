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
  useDisclosure,
} from "@nextui-org/react";
import { PackagePlus, Trash2 } from "lucide-react";
import ProductMotificationPage from "./product-motification/page";
import { useProductId } from "@/state/state";
import SectionHeader from "@/components/section_header";
import { shopProductlist } from "@/data/data";

const columns: ITableColumProp[] = [
  {
    key: "index",
    label: "Index",
  },
  {
    key: "item",
    label: "Item",
  },
  {
    key: "price",
    label: "Price",
  },
  {
    key: "action",
    label: "Actions",
  },
];

const ProductAnalyzePage = () => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const { setProductId } = useProductId();

  const rows = shopProductlist.map((product) => ({
    key: product.id,
    index: product.id,
    item: (
      <CartItemCard
        product={product}
        onClick={() => {
          setProductId(product.id);
          onOpen();
        }}
      />
    ),
    price: `$${product.price.toFixed(2)}`,
  }));

  return (
    <>
      <SectionHeader
        title={"Products"}
        action={
          <Button
            className="text-white bg-black h-10"
            onPress={() => {
              setProductId("");
              onOpen();
            }}
          >
            <PackagePlus />
            <span>Create new</span>
          </Button>
        }
        content={
          <Table aria-label="Cart table" className="mb-8">
            <TableHeader columns={columns}>
              {(column) => (
                <TableColumn key={column.key}>{column.label}</TableColumn>
              )}
            </TableHeader>
            <TableBody items={rows}>
              {(item) => (
                <TableRow key={item.key}>
                  {(columnKey) => (
                    <TableCell>
                      {columnKey === "action" ? (
                        <Button
                          variant="light"
                          color="danger"
                          isIconOnly
                          // onClick={() => handleDelete(item.key)}
                        >
                          <Trash2 />
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
        }
      />

      <ProductMotificationPage isOpen={isOpen} onOpenChange={onOpenChange} />
    </>
  );
};

export default ProductAnalyzePage;
