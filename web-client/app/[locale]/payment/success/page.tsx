"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@nextui-org/react";
import orderAPIs from "@/api/order";
import { CircleCheck } from "lucide-react";

const PaymentSuccessPage = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const orderId = searchParams.get("order_id");

  const handleContinueShopping = () => {
    router.push("/products");
  };

  const handleViewOrder = () => {
    if (orderId) {
      router.push(`/order/${orderId}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-8">
      <CircleCheck color="green" size={80} />
      <h1 className="text-3xl font-bold">Payment Successful!</h1>
      <div className="flex gap-4">
        <Button 
          className="bg-black text-white px-8" 
          onClick={handleContinueShopping}
        >
          Continue Shopping
        </Button>
        <Button
          variant="bordered"
          onClick={handleViewOrder}
          disabled={!orderId}
        >
          View Order
        </Button>
      </div>
    </div>
  );
};

export default PaymentSuccessPage; 