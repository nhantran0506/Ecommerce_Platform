"use client";
import ProductCard from "@/components/product_card";
import { IProduct } from "@/interface/IProduct";

const ProductPage = () => {
  // Fake product data
  const productlist: IProduct[] = [
    {
      id: 1,
      name: "Wireless Headphones",
      description:
        "High-quality wireless headphones with noise-canceling feature.",
      price: 99.99,
      image:
        "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
    },
    {
      id: 2,
      name: "Smartphone",
      description: "Latest model with advanced camera and fast performance.",
      price: 699.99,
    },
    {
      id: 3,
      name: "Gaming Laptop",
      description:
        "Powerful laptop with a high-refresh-rate screen and strong GPU.",
      price: 1299.99,
    },
    {
      id: 4,
      name: "Smartwatch",
      description:
        "Water-resistant smartwatch with fitness tracking and notifications.",
      price: 199.99,
    },
    {
      id: 5,
      name: "Bluetooth Speaker",
      description: "Portable speaker with deep bass and long battery life.",
      price: 49.99,
    },
    {
      id: 6,
      name: "4K TV",
      description:
        "Ultra HD 4K television with vibrant colors and smart TV features.",
      price: 499.99,
    },
  ];

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {productlist.map((item) => (
          <ProductCard key={item.id} product={item} />
        ))}
      </div>
    </div>
  );
};

export default ProductPage;
