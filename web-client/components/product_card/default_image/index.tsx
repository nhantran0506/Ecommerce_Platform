import defaultImage from "@/assets/defaultImage.png";
import { ImageSizeEnum, IProductDefaultImage } from "@/interface/UI/IProductUI";
import Image from "next/image";

const DefaultImage: React.FC<IProductDefaultImage> = ({ imgSize }) => {
  const applyImageSize = (size: ImageSizeEnum) => {
    switch (size) {
      case ImageSizeEnum.lg:
        return "w-44 h-44";
      case ImageSizeEnum.md:
        return "w-24 h-24";
      case ImageSizeEnum.sm:
        return "w-16 h-16";
      default:
        return "w-24 h-24";
    }
  };

  return (
    <div className="w-full h-full bg-gray-300 flex items-center justify-center rounded-xl">
      <Image
        src={defaultImage}
        alt="default_image"
        className={applyImageSize(imgSize)}
      />
    </div>
  );
};

export default DefaultImage;
