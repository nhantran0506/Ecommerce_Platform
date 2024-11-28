"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import DefaultImage from "@/components/product_card/default_image";
import {
  Calendar,
  Heart,
  Minus,
  Plus,
  Star,
  ShoppingCart,
  Home,
  Tag,
} from "react-feather";
import {
  ImageSizeEnum,
  IProductIconDataSection,
} from "@/interface/UI/IProductUI";
import {
  Button,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  useDisclosure,
} from "@nextui-org/react";
import productAPIs from "@/api/product";
import cartAPIs from "@/api/cart";
import { CircleCheck } from "lucide-react";
// import { IProductData } from "@/interface/Data/IProductData";
// import { productlist } from "@/data/data";

const ProductDetailPage = ({ params }: { params: { id: string } }) => {
  const maxNumberOfProduct = 10;
  const [product, setProduct] = useState<IProductDetailData | null>(null);
  const [loading, setLoading] = useState(false);
  const [numberOfProduct, setNumberOfProduct] = useState<number>(1);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  useEffect(() => {
    const fetchProductDetail = async () => {
      try {
        const res = await productAPIs.getProductById(params.id);
        setProduct(res);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };

    setLoading(true);
    fetchProductDetail();
  }, [params.id]);

  const handleAddToCart = async () => {
    try {
      // const reqBody: IReqAddToCart = {
      //   product_id: params.id,
      //   quantity: numberOfProduct,
      // };

      // const res = await cartAPIs.addToCart(reqBody);

      // if (res) {
      onOpen();
      // }
    } catch (error) {
      console.error("Failed to fetch products:", error);
    } finally {
      setLoading(false);
    }
  };

  const listCategoryDataSection: IProductIconDataSection[] =
    product?.product_category?.map((category) => ({
      prefix: <Tag />,
      data: category,
    })) ?? [];

  const listOtherDataSection: IProductIconDataSection[] = [
    // {
    //   prefix: <Calendar />,
    //   data: new Date(product?.create_at_datetime!).toLocaleString(),
    // },
    // {
    //   prefix: <Star />,
    //   data: "4.8",
    //   subText: "1823",
    //   isHightlight: true,
    // },
    // {
    //   prefix: <Home />,
    //   data: maxNumberOfProduct.toString(),
    // },
  ];

  const listIconDataSection: IProductIconDataSection[] = [
    ...listCategoryDataSection,
    ...listOtherDataSection,
  ];

  const IconDataSection = ({
    prefix,
    data,
    subText,
    isHightlight,
  }: IProductIconDataSection) => (
    <div className="flex gap-2 mb-4">
      {prefix}
      <div className="flex items-center">
        <p className={isHightlight ? "font-bold" : ""}>{data}</p>
        {subText && <span className="text-sm text-gray-500">({subText})</span>}
      </div>
    </div>
  );

  const ProductNumberPickerSection = () => (
    <div className="flex items-center gap-4">
      <Button
        isIconOnly
        radius="lg"
        className="bg-slate-200"
        onClick={() =>
          setNumberOfProduct((numberOfProduct) =>
            numberOfProduct >= 1 ? numberOfProduct - 1 : 0
          )
        }
      >
        <Minus size={15} />
      </Button>
      <p>{numberOfProduct}</p>
      <Button
        isIconOnly
        radius="lg"
        className="bg-slate-200"
        onClick={() =>
          setNumberOfProduct((numberOfProduct) =>
            numberOfProduct < maxNumberOfProduct
              ? numberOfProduct + 1
              : maxNumberOfProduct
          )
        }
      >
        <Plus size={15} />
      </Button>
    </div>
  );

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex mb-1 gap-2 items-center text-2xl">
                Congratuation! <CircleCheck color="green" size={30} />
              </ModalHeader>
              <ModalBody className="mb-2">
                <div>Add to cart successfully!</div>
              </ModalBody>
              <ModalFooter>
                <Button color="primary" onPress={onClose}>
                  Ok
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>

      <div className="mx-64 grid grid-cols-2 mt-20">
        <div className="rounded-lg bg-transparent overflow-hidden w-[450px] h-[400px] relative">
          {product.image_urls[0] ? (
            <Image
              src={product.image_urls[0]}
              alt="Product image"
              layout="fill"
              className="object-cover"
              priority={true}
            />
          ) : (
            <DefaultImage imgSize={ImageSizeEnum.lg} />
          )}
        </div>

        <div className="flex flex-col justify-between">
          <div className="px-2 pt-2">
            <div className="flex justify-between mb-4">
              <h1 className="font-bold text-2xl">{product.product_name}</h1>

              <div className="w-9 h-9 border-2 border-slate-300 rounded-full flex items-center justify-center">
                <Heart size={20} />
              </div>
            </div>

            <p className="font-bold text-2xl mb-4">${product.price}</p>

            <p className="mb-4">{product.product_description}</p>

            <div className="grid grid-cols-2 mb-4">
              {product.product_category.length > 0 &&
                listIconDataSection.map((item, index) => (
                  <IconDataSection
                    key={index}
                    prefix={item.prefix}
                    data={item.data}
                    subText={item.subText}
                    isHightlight={item.isHightlight}
                  />
                ))}
            </div>

            <ProductNumberPickerSection />
          </div>

          <div className="flex gap-4">
            <Button
              className="bg-black text-white px-24 font-bold"
              radius="full"
            >
              Order Now
            </Button>
            <Button
              className="font-bold px-5"
              variant="bordered"
              radius="full"
              onClick={() => handleAddToCart()}
            >
              <span className="text-gray-400">
                <ShoppingCart color="currentColor" fill="currentColor" />
              </span>{" "}
              Add to Cart
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProductDetailPage;
