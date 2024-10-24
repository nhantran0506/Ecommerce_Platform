import { OrderStatus } from "@/constant/enum";
import { IOrder } from "@/interface/Data/IOrderData";
import { IProductData, IShopProductData } from "@/interface/Data/IProductData";

export const listOrderItem: IOrder[] = [
  {
    id: "0",
    status: OrderStatus.completed,
    listOrderItem: [
      {
        product: {
          id: "0",
          product_name: "Colorful true-beauty natural wild iguana",
          product_description:
            "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
          price: 99.99,
          image:
            "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
          create_at_datetime: "2019-01-16",
        },
        number: 3,
      },
      {
        product: {
          id: "1",
          product_name: "Smartphone",
          product_description:
            "Latest model with advanced camera and fast performance.",
          image:
            "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
          price: 699.99,
        },
        number: 1,
      },
    ],
  },
  {
    id: "1",
    status: OrderStatus.transport,
    listOrderItem: [
      {
        product: {
          id: "0",
          product_name: "Colorful true-beauty natural wild iguana",
          product_description:
            "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
          price: 99.99,
          image:
            "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
          create_at_datetime: "2019-01-16",
        },
        number: 3,
      },
      {
        product: {
          id: "1",
          product_name: "Smartphone",
          product_description:
            "Latest model with advanced camera and fast performance.",
          price: 699.99,
        },
        number: 1,
      },
    ],
  },
  {
    id: "2",
    status: OrderStatus.ordered,
    listOrderItem: [
      {
        product: {
          id: "0",
          product_name: "Colorful true-beauty natural wild iguana",
          product_description:
            "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
          price: 99.99,
          image:
            "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
          create_at_datetime: "2019-01-16",
        },
        number: 3,
      },
      {
        product: {
          id: "1",
          product_name: "Smartphone",
          product_description:
            "Latest model with advanced camera and fast performance.",
          price: 699.99,
        },
        number: 1,
      },
    ],
  },
];

export const shopProductlist: IShopProductData[] = [
  {
    id: "0",
    product_name: "Colorful true-beauty natural wild iguana",
    product_description:
      "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
    price: 99.99,
    image:
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    create_at_datetime: "2019-01-16",
    lastUpdate: "2024-10-11",
  },
  {
    id: "1",
    product_name: "Smartphone",
    product_description:
      "Latest model with advanced camera and fast performance.",
    price: 699.99,
    lastUpdate: "2024-10-12",
  },
  {
    id: "2",
    product_name: "Gaming Laptop",
    product_description:
      "Powerful laptop with a high-refresh-rate screen and strong GPU.",
    price: 1299.99,
    lastUpdate: "2024-10-13",
  },
  {
    id: "3",
    product_name: "Smartwatch",
    product_description:
      "Water-resistant smartwatch with fitness tracking and notifications.",
    price: 199.99,
    lastUpdate: "2024-10-14",
  },
  {
    id: "4",
    product_name: "Bluetooth Speaker",
    product_description:
      "Portable speaker with deep bass and long battery life.",
    price: 49.99,
    lastUpdate: "2024-10-15",
  },
  {
    id: "5",
    product_name: "4K TV",
    product_description:
      "Ultra HD 4K television with vibrant colors and smart TV features.",
    price: 499.99,
    lastUpdate: "2024-10-16",
  },
];

export const productlist: IProductData[] = [
  {
    id: "0",
    product_name: "Colorful true-beauty natural wild iguana",
    product_description:
      "High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature. High-quality wireless headphones with noise-canceling feature.",
    price: 99.99,
    image:
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    create_at_datetime: "2019-01-16",
  },
  {
    id: "1",
    product_name: "Smartphone",
    product_description:
      "Latest model with advanced camera and fast performance.",
    price: 699.99,
  },
  {
    id: "2",
    product_name: "Gaming Laptop",
    product_description:
      "Powerful laptop with a high-refresh-rate screen and strong GPU.",
    price: 1299.99,
  },
  {
    id: "3",
    product_name: "Smartwatch",
    product_description:
      "Water-resistant smartwatch with fitness tracking and notifications.",
    price: 199.99,
  },
  {
    id: "4",
    product_name: "Bluetooth Speaker",
    product_description:
      "Portable speaker with deep bass and long battery life.",
    price: 49.99,
  },
  {
    id: "5",
    product_name: "4K TV",
    product_description:
      "Ultra HD 4K television with vibrant colors and smart TV features.",
    price: 499.99,
  },
];

export const recommendProductlist: IProductData[] = [
  {
    id: "0",
    product_name: "Wireless Headphones",
    product_description:
      "High-quality wireless headphones with noise-canceling feature.",
    price: 99.99,
    image:
      "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    create_at_datetime: "2019-01-16",
  },
  {
    id: "1",
    product_name: "Smartphone",
    product_description:
      "Latest model with advanced camera and fast performance.",
    price: 699.99,
  },
  {
    id: "2",
    product_name: "Gaming Laptop",
    product_description:
      "Powerful laptop with a high-refresh-rate screen and strong GPU.",
    price: 1299.99,
  },
];
