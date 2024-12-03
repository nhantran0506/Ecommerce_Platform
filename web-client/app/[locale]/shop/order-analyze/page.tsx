"use client";

import OrderCard from "@/components/order_card";
import SectionHeader from "@/components/section_header";
import { useEffect, useState } from "react";
import orderAPIs from "@/api/order";
import Spinner from "@/components/spinner";
import { OrderStatus } from "@/constant/enum";
import { Card, Skeleton } from "@nextui-org/react";

const OrderAnalyzePage = () => {
  const [orders, setOrders] = useState<IOrderHistory[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        const data = await orderAPIs.getOrderHistory();
        setOrders(data);
      } catch (error) {
        console.error("Failed to fetch orders:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) {
    return <OrderAnalyzeSkeleton />;
  }

  return (
    <SectionHeader
      title="Order History"
      content={
        <div className="grid grid-cols-2 gap-4">
          {orders.map((order, index) => (
            <OrderCard
              key={order.order_id}
              index={index.toString()}
              status={OrderStatus.completed} // Adjust status as needed
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
          ))}
        </div>
      }
    />
  );
};

const OrderAnalyzeSkeleton = () => {
  return (
    <div className="grid grid-cols-2 gap-4">
      {Array(4)
        .fill(null)
        .map((_, index) => (
          <Card key={index} className="p-4">
            <div className="flex justify-between mb-4">
              <Skeleton className="w-24 h-6 rounded-lg" />
              <Skeleton className="w-32 h-6 rounded-lg" />
            </div>

            {Array(2)
              .fill(null)
              .map((_, itemIndex) => (
                <div key={itemIndex} className="flex items-center gap-4 mb-4">
                  <Skeleton className="w-20 h-20 rounded-lg" />
                  <div className="flex-1">
                    <Skeleton className="w-3/4 h-4 rounded-lg mb-2" />
                    <Skeleton className="w-1/4 h-4 rounded-lg" />
                  </div>
                </div>
              ))}

            <div className="flex justify-between mt-4">
              <Skeleton className="w-32 h-6 rounded-lg" />
              <Skeleton className="w-24 h-6 rounded-lg" />
            </div>
          </Card>
        ))}
    </div>
  );
};

export default OrderAnalyzePage;
