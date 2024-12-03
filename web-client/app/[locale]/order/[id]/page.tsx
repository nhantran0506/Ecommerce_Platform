"use client";

import CartItemCard from "@/components/cart_item_card";
import SectionHeader from "@/components/section_header";
import { listOrderItem } from "@/data/data";
import { IOrder } from "@/interface/Data/IOrderData";
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  Divider,
  getKeyValue,
  Progress,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
} from "@nextui-org/react";
import { useEffect, useState } from "react";

interface IOrderStep {
  orderStep: string[];
  currentStep: number;
}

const listOrderStep: IOrderStep = {
  orderStep: [
    "Order confirming",
    "Payment pending",
    "Progressing",
    "Shipping",
    "Delivered",
  ],
  currentStep: 2,
};

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
    key: "quantity",
    label: "Quantity",
  },
];

const OrderDetailPage = ({ params }: { params: { id: string } }) => {
  const [order, setOrder] = useState<IOrder | null>(null);

  useEffect(() => {
    setOrder(listOrderItem[Number(params.id)]);
  }, [params.id]);

  const rows =
    order?.listOrderItem?.map((item, index) => ({
      key: index,
      index: index,
      item: (
        <CartItemCard
          product={{
            ...item.product,
            quantity: item.number,
          }}
          onClick={() => {}}
        />
      ),
      price: item?.product?.price ? `$${item.product.price.toFixed(2)}` : "N/A",
      quantity: item.number,
    })) || [];

  return (
    <div className="flex flex-col mx-60 my-10">
      <h1 className="text-3xl font-bold mb-8">OrderDetailPage #{order?.id}</h1>

      <SectionHeader
        title={"Progress"}
        content={
          <div>
            <Card>
              <CardBody>
                <div className="flex gap-4">
                  {listOrderStep.orderStep.map((item, index) => (
                    <Progress
                      key={index}
                      aria-label="Loading..."
                      label={item}
                      value={index <= listOrderStep.currentStep ? 100 : 0}
                      className="max-w-md"
                    />
                  ))}
                </div>
              </CardBody>
              <Divider />
              <CardFooter className="flex justify-between">
                <Button radius="full" variant="bordered">
                  Estimated shipping date:{" "}
                  <span className="font-semibold">20 Oct, 2024</span>
                </Button>
                <Button radius="full" className="bg-black text-white">
                  Mask as received
                </Button>
              </CardFooter>
            </Card>
          </div>
        }
      />

      <SectionHeader
        title={"Products"}
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
                    <TableCell>{getKeyValue(item, columnKey)}</TableCell>
                  )}
                </TableRow>
              )}
            </TableBody>
          </Table>
        }
      />
    </div>
  );
};

export default OrderDetailPage;
