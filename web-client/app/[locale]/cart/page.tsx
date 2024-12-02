"use client";
import CartItemCard from "@/components/cart_item_card";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  getKeyValue,
  Button,
  Divider,
  Card,
  CardBody,
} from "@nextui-org/react";
import { ChevronLeft, X } from "react-feather";
import ProductNumberPicker from "@/components/product_number_picker";
import { useEffect, useState } from "react";
import cartAPIs from "@/api/cart";
import orderAPIs from "@/api/order";
import { useRouter } from "next/navigation";

const CartPage = () => {
  const router = useRouter();

  const [loading, setLoading] = useState(false);
  const [productlist, setProductList] = useState<IProductInCart[]>();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);

        const res = await cartAPIs.getProductInCart();

        setProductList(res.cart_details.products);
      } catch (error) {
        console.error("Failed to fetch products in cart:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleAddToCart = async (id: string, val: number) => {
    try {
      const reqBody: IReqAddToCart = {
        product_id: id,
        quantity: val,
      };

      await cartAPIs.addToCart(reqBody);

      console.log(`Update ${id} with value ${val}`);
    } catch (error) {
      console.error("Failed to fetch products:", error);
    } finally {
      setLoading(false);
    }
  };

  const rows = productlist?.map((product) => ({
    key: product.product_id,
    item: <CartItemCard product={product} onClick={() => {}} />,
    price: `$${product.price.toFixed(2)}`,
    quantity: (
      <div className="flex justify-center items-center">
        <ProductNumberPicker
          id={product.product_id}
          value={product.quantity}
          setValue={(id, value) => handleAddToCart(id, value)}
          maxNumberOfProduct={20}
        />
      </div>
    ),
    total_price: `$${product.total_price.toFixed(2)}`,
  }));

  const columns: ITableColumProp[] = [
    {
      key: "item",
      label: "Item",
    },
    {
      key: "price",
      label: "Price",
    },
    {
      key: "quantity",
      label: "Quantity",
    },
    {
      key: "total_price",
      label: "Total Price",
    },
    {
      key: "options",
      label: "",
    },
  ];

  const totalPriceOfAllCart = (
    productlist: IProductInCart[] | undefined
  ): number => {
    if (productlist)
      return productlist?.reduce((sum, item) => sum + item.total_price, 0);

    return 0;
  };

  const handleCheckOut = async () => {
    try {
      setLoading(true);

      const reqBody: IOrderProduct[] = productlist
        ? productlist.map(({ product_id, quantity }) => ({
            product_id,
            quantity,
          }))
        : [];

      const res = await orderAPIs.checkout(reqBody);

      if (res) {
        router.push("/cart/complete");
      }
    } catch (error) {
      console.error("Failed to fetch products:", error);
    } finally {
      setLoading(false);
    }
  };

  return loading ? (
    <div className="text-center">Loading...</div>
  ) : (
    <div className="flex flex-col justify-center mx-64">
      <h1 className="flex gap-2 font-bold text-xl mb-4 mt-12">
        Cart
        <span className="text-[#939699] font-normal">
          ({productlist?.length})
        </span>
      </h1>

      {productlist?.length! > 0 ? (
        <Table aria-label="Cart table" className="mb-8">
          <TableHeader columns={columns}>
            {(column) => (
              <TableColumn key={column.key}>
                <p
                  className={`text-sm ${
                    column.key === "quantity" ? "text-center" : ""
                  }`}
                >
                  {column.label}
                </p>
              </TableColumn>
            )}
          </TableHeader>
          <TableBody items={rows}>
            {(item) => (
              <TableRow key={item.key}>
                {(columnKey) => (
                  <TableCell>
                    {columnKey === "options" ? (
                      <Button
                        variant="light"
                        color="danger"
                        isIconOnly
                        // onClick={() => handleDelete(item.key)}
                      >
                        <X />
                      </Button>
                    ) : (
                      getKeyValue(item, columnKey)
                    )}
                  </TableCell>
                )}
              </TableRow>
            )}
          </TableBody>
        </Table>
      ) : (
        <div>Loading...</div>
      )}

      <Divider className="mb-8" />

      <div className="mb-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ChevronLeft size={18} className="text-[#BCBFC2]" />
          <p className="text-[#939699] font-bold">Back to shopping</p>
        </div>

        <div className="flex items-center gap-4">
          <p>
            Total Price:{" "}
            <span className="font-bold">
              ${totalPriceOfAllCart(productlist)}
            </span>
          </p>

          <Button
            onClick={() => handleCheckOut()}
            className="text-white bg-black rounded-full py-2 px-8 font-bold"
          >
            Checkout
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
