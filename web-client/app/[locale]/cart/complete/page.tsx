import { Button } from "@nextui-org/react";
import DevileryMan from "@/assets/DevileryMan.png";
import Image from "next/image";

const CheckoutCompletePage = () => {
  return (
    <div className="w-full flex items-start justify-center gap-10 py-16">
      <Image
        src={DevileryMan}
        alt="devilery-man-icon"
        width={160}
        height={160}
      />
      <div>
        <p className="font-semibold text-lg mb-4">Order successful</p>
        <h1 className="font-bold text-3xl mb-4">Thank you for your order!</h1>
        <p className="text-xl mb-4">
          Order number is: <span className="font-bold">#{"123456"}</span>
        </p>
        <p className="text-sm mb-4">
          You can track your order in “My Order” section
        </p>

        <div className="flex gap-4">
          <Button className="rounded-full text-white bg-black px-6 font-bold">
            Track my order
          </Button>
          <Button
            className="rounded-full text-black bg-white px-6 font-bold"
            variant="bordered"
          >
            Continue shopping
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CheckoutCompletePage;
