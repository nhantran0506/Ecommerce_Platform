import ProductCard from "@/components/product_card";

export default function Home() {
  return (
    <div>
      <h1>Home Page</h1>
      <ProductCard
        title={
          "Chocolate CheesecakeCheesecake Cheesecake CheesecakeCheesecakeCheesecakeCheesecakeCheesecake"
        }
        img={"https://nextui.org/images/hero-card-complete.jpeg"}
        price={10}
        key={0}
      />
    </div>
  );
}
