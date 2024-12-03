import { OrderStatus } from "@/constant/enum";
import { IOrder } from "@/interface/Data/IOrderData";
// import { IShopProductData } from "@/interface/Data/IProductData";

export const listOrderItem: IOrder[] = [
  {
    id: "0",
    status: OrderStatus.completed,
    listOrderItem: [
      {
        product: {
          product_id: "0",
          product_name: "Colorful true-beauty natural wild iguana",
          product_price: 99.99,
          image_urls: [
            "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
          ],
        },
        number: 3,
      },
      {
        product: {
          product_id: "1",
          product_name: "Colorful true-beauty natural wild iguana",
          product_price: 99.99,
          image_urls: [
            "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
          ],
        },
        number: 3,
      },
    ],
  },
];

export const shopProductlist: IProductTable[] = [
  {
    product_id: "0",
    product_name: "Colorful true-beauty natural wild iguana",
    price: 99.99,
    image_urls: [
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    ],
    quantity: 1,
  },
  {
    product_id: "1",
    product_name: "Colorful true-beauty natural wild iguana",
    price: 99.99,
    image_urls: [
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    ],
    quantity: 2,
  },
];

export const productlist: IProductData[] = [
  {
    product_name: "Colorful true-beauty natural wild iguana",
    // product_description:
    //   "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
    product_price: 99.99,
    image_urls: [
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    ],
    product_id: "0",
  },
  {
    product_name: "San pham A",
    // product_description:
    //   "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
    product_price: 99.99,
    image_urls: [
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    ],
    product_id: "0",
  },
  {
    product_name: "San pham B",
    // product_description:
    //   "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
    product_price: 99.99,
    image_urls: [
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    ],
    product_id: "0",
  },
];
