"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@nextui-org/react";
import { XCircle } from "react-feather";
import orderAPIs from "@/api/order";

const getErrorMessage = (code: string) => {
  const errorMessages: { [key: string]: string } = {
    "07": "Transaction is suspicious (related to fraud or unusual activity).",
    "09": "Transaction failed: Card/Account not registered for Internet Banking.",
    "10": "Transaction failed: Incorrect card/account authentication (3 attempts).",
    "11": "Transaction failed: Payment timeout. Please try again.",
    "12": "Transaction failed: Card/Account is locked.",
    "13": "Transaction failed: Incorrect OTP. Please try again.",
    "24": "Transaction cancelled by user.",
    "51": "Transaction failed: Insufficient balance.",
    "65": "Transaction failed: Daily transaction limit exceeded.",
    "75": "Payment bank is under maintenance.",
    "79": "Transaction failed: Exceeded password attempts.",
    "99": "Transaction failed: Other error.",
  };

  return errorMessages[code] || "Transaction failed. Please try again.";
};

const PaymentFailedPage = () => {
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

      if (responseCode === "00") {
        router.push("/payment/success" + window.location.search);
        return;
      }

      try {
        // Restore the order if payment failed
        await orderAPIs.restoreOrder(orderId);
      } catch (error) {
        console.error("Failed to restore order:", error);
      }
    };

    handlePaymentResult();
  }, [searchParams, router]);

  const responseCode = searchParams.get("vnp_ResponseCode") || "";

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 text-center">
        <div className="flex justify-center">
          <XCircle size={64} className="text-red-500" />
        </div>
        
        <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
          Payment Failed
        </h2>
        
        <p className="text-gray-600 mt-2">
          {getErrorMessage(responseCode)}
        </p>

        <div className="mt-6 flex gap-4 justify-center">
          <Button
            onClick={() => router.push("/cart")}
            className="bg-black text-white font-semibold rounded-full px-8"
          >
            Return to Cart
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

export default PaymentFailedPage; 