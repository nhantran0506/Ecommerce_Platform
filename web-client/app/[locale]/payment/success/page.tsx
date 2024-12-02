"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@nextui-org/react";
import { CheckCircle } from "react-feather";

const PaymentSuccessPage = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [orderId, setOrderId] = useState<string>("");

  useEffect(() => {
    // Get order ID from URL params if provided by payment gateway
    const orderIdParam = searchParams.get("order_id");
    if (orderIdParam) {
      setOrderId(orderIdParam);
    }
  }, [searchParams]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 text-center">
        <div className="flex justify-center">
          <CheckCircle size={64} className="text-green-500" />
        </div>
        
        <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
          Payment Successful!
        </h2>
        
        {orderId && (
          <p className="text-gray-600">
            Order ID: <span className="font-semibold">{orderId}</span>
          </p>
        )}

        <p className="text-gray-600 mt-2">
          Thank you for your purchase. Your payment has been processed successfully.
        </p>

        <div className="mt-6 flex gap-4 justify-center">
          <Button
            onClick={() => router.push("/orders")}
            className="bg-black text-white font-semibold rounded-full px-8"
          >
            View Orders
          </Button>
          
          <Button
            onClick={() => router.push("/products")}
            variant="bordered"
            className="font-semibold rounded-full px-8"
          >
            Continue Shopping
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PaymentSuccessPage; 