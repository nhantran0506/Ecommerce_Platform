import defaultImage from "@/assets/defaultImage.png";
import Image from "next/image";

const DefaultImage = () => {
  return (
    <div className="w-full h-[200px] bg-gray-300 flex items-center justify-center">
      <Image src={defaultImage} alt="default_image" className="w-20 h-20" />
    </div>
  );
};

export default DefaultImage;
