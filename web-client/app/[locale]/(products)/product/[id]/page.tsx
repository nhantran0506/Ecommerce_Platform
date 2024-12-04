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
import ProductDetailSkeleton from "@/components/product_detail_skeleton";
import RatingInput from "@/components/product_rating/rating_input";
import ExpandableDescription from "@/components/expandable_description";
import RatingList from "@/components/product_rating/rating_list";
import StarRating from "@/components/start_rating";
// import ProductDetailSkeleton from "@/components/product_detail/product_detail_skeleton";

const ProductDetailPage = ({ params }: { params: { id: string } }) => {
  const maxNumberOfProduct = 10;
  const [product, setProduct] = useState<IProductDetailData | null>(null);
  const [loading, setLoading] = useState(false);
  const [numberOfProduct, setNumberOfProduct] = useState<number>(1);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const productId = params?.id;

  const [ratings, setRatings] = useState<IProductRatingResponse[]>([]);
  const [isAddingToCart, setIsAddingToCart] = useState(false);

  useEffect(() => {
    const fetchProductDetail = async () => {
      if (!productId) return;

      try {
        setLoading(true);
        const res = await productAPIs.getProductById(productId);
        setProduct(res);
      } catch (error) {
        console.log("Failed to fetch products:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProductDetail();
  }, [productId]);

  useEffect(() => {
    const fetchComments = async () => {
      if (!productId) return;
      try {
        const comments = await productAPIs.getProductComments(productId);
        setRatings(comments);
      } catch (error) {
        console.error("Failed to fetch comments:", error);
      }
    };

    fetchComments();
  }, [productId]);

  const handleAddToCart = async () => {
    try {
      setIsAddingToCart(true);
      const reqBody: ICartModify[] = [
        {
          product_id: productId,
          quantity: numberOfProduct,
        },
      ];

      await cartAPIs.updateCart(reqBody);
      
      // Show success animation
      const cartButton = document.querySelector('.cart-button');
      if (cartButton) {
        cartButton.classList.add('cart-animation');
        setTimeout(() => {
          cartButton.classList.remove('cart-animation');
          onOpen(); // Show success modal
        }, 1000);
      }
    } catch (error) {
      console.log("Failed to add to cart:", error);
    } finally {
      setIsAddingToCart(false);
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

  const handleRatingSubmit = async (rating: number, comment: string) => {
    try {
      setLoading(true);
      await productAPIs.productRating({
        product_id: productId,
        rating,
        comment,
      });
      
      // Refresh comments after successful submission
      const updatedComments = await productAPIs.getProductComments(productId);
      setRatings(updatedComments);
      
      return { success: true };
    } catch (error: any) {
      if (error.response?.status === 403) {
        return { 
          success: false, 
          error: "You need to purchase this product before you can leave a review." 
        };
      }
      console.error("Failed to submit rating:", error);
      return { 
        success: false, 
        error: "An error occurred while submitting your review." 
      };
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <ProductDetailSkeleton />;
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

      <div className="mx-64 flex flex-col mt-20">
        <div className="grid grid-cols-2 gap-8 mb-8">
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
                <div>
                  <h1 className="font-bold text-2xl mb-2">{product.product_name}</h1>
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <StarRating 
                        totalStars={5} 
                        initStart={product.product_avg_stars} 
                        readonly={true}
                      />
                      <span className="text-gray-500">
                        ({product.product_total_ratings} ratings)
                      </span>
                    </div>
                    <div className="text-gray-500">
                      {product.product_total_sales} sold
                    </div>
                  </div>
                </div>
              </div>

              <p className="font-bold text-2xl mb-4">${product.price}</p>

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
                onClick={() => handleAddToCart()}
              >
                Order Now
              </Button>
              <Button
                className="font-bold px-5 cart-button"
                variant="bordered"
                radius="full"
                onClick={() => handleAddToCart()}
                disabled={isAddingToCart}
              >
                <span className="text-gray-400">
                  <ShoppingCart 
                    color="currentColor" 
                    fill="currentColor"
                    className={isAddingToCart ? 'animate-bounce' : ''}
                  />
                </span>
                Add to Cart
              </Button>
            </div>
          </div>
        </div>

        <div className="w-full">
          <h2 className="text-xl font-bold mb-4">Product Description</h2>
          <ExpandableDescription description={product.product_description} />
        </div>

        <div className="mt-8 space-y-8">
          <RatingInput onSubmit={handleRatingSubmit} />
          <RatingList ratings={ratings} />
        </div>
      </div>
    </>
  );
};

export default ProductDetailPage;
