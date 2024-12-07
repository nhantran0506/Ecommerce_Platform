"use client";

import orderAPIs from "@/api/order";
import CartItemCard from "@/components/cart_item_card";
import SectionHeader from "@/components/section_header";
import { formatDate } from "@/libraries/helpers";
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
  currentStep: 3,
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
  const [loading, setLoading] = useState(false);
  const [order, setOrder] = useState<IOrderDetails | null>(null);

  useEffect(() => {
    fetchOrderDetail();
  }, [params.id]);

  const fetchOrderDetail = async () => {
    try {
      setLoading(true);
      const res = await orderAPIs.getOrderById(params.id);
      setOrder(res);
    } catch (error) {
      console.log("Failed to fetch products:", error);
    } finally {
      setLoading(false);
    }
  };

  const rows =
    order?.product?.map((item, index) => ({
      key: index,
      index: index,
      // item: <CartItemCard product={item} onClick={() => {}} />,
      item: <div className="font-bold text-base">{item.product_name}</div>,
      price: item?.total ? `$${item.total.toFixed(2)}` : "N/A",
      quantity: item.quantity,
    })) || [];

  if (loading) {
    return <></>;
  }

  return (
    <div className="flex flex-col mx-60 my-10">
      <h1 className="text-3xl font-bold mb-8">
        OrderDetailPage #{order?.order_id}
      </h1>

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
                  <span className="font-semibold">
                    {formatDate(order?.created_at ?? "")}
                  </span>
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
