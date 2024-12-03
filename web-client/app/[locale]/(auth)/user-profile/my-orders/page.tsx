"use client";

import OrderCard from "@/components/order_card";
import SectionHeader from "@/components/section_header";
import { OrderStatus } from "@/constant/enum";
import orderAPIs from "@/api/order";
import { useEffect, useState } from "react";
import { IOrderHistory } from "@/interface/Data/IOrderData";
import { Card, Skeleton } from "@nextui-org/react";

const MyOrdersPage = () => {
  const [orders, setOrders] = useState<IOrderHistory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await orderAPIs.getOrderHistory();
        setOrders(data);
      } catch (error) {
        console.error("Failed to fetch orders:", error);
        setError("Failed to load orders. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-2 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="p-4">
            <Skeleton className="w-full h-32 rounded-lg" />
          </Card>
        ))}
      </div>
    );
  }

  if (error) {
    return <div className="text-center text-red-500 py-8">{error}</div>;
  }

  return (
    <SectionHeader
      title="Order History"
      content={
        <div className="grid grid-cols-2 gap-4">
          {orders.length > 0 ? (
            orders.map((order) => (
              <OrderCard
                key={order.order_id}
                index={order.order_id}
                status={OrderStatus.completed} // You might want to add status to your IOrderHistory interface
                listOrderItem={order.product.map((product) => ({
                  product: {
                    product_id: product.product_id,
                    product_name: product.product_name,
                    price: product.price,
                    image_urls: [], // Add image URLs if available from API
                  },
                  number: product.quantity,
                }))}
                createdAt={order.created_at}
              />
            ))
          ) : (
            <div className="col-span-2 text-center py-8">No orders found</div>
          )}
        </div>
      }
    />
  );
};

export default MyOrdersPage;
