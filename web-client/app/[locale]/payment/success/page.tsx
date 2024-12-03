"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@nextui-org/react";
import { CheckCircle } from "react-feather";
import orderAPIs from "@/api/order";

const PaymentSuccessPage = () => {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const handlePaymentResult = async () => {
      const responseCode = searchParams.get("vnp_ResponseCode");
      const orderId = searchParams.get("vnp_TxnRef");

      if (!responseCode || !orderId) {
        router.push("/products");
        return;
      }

      // Only response code "00" indicates success
      // All other codes indicate various types of failures
      if (responseCode !== "00") {
        router.push("/payment/failed" + window.location.search);
        return;
      }

      try {
        // Get order details using the order ID
        const orderDetails = await orderAPIs.getOrderById(orderId);
        // You can use orderDetails here if needed
      } catch (error) {
        console.error("Failed to fetch order details:", error);
      }
    };

    handlePaymentResult();
  }, [searchParams, router]);

  const orderId = searchParams.get("vnp_TxnRef");

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
            Order ID: <span className="font-semibold">#{orderId}</span>
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