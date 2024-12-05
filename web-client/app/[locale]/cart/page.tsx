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
import ProductListInCartSkeleton from "@/components/list_product_in_card_skeleton";

const CartPage = () => {
  const router = useRouter();

  const [loading, setLoading] = useState(false);
  const [productlist, setProductList] = useState<IProductTable[]>();
  const [cartData, setCartData] = useState<IResCartProductList | null>(null);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        setLoading(true);
        const data = await cartAPIs.getProductInCart();
        setCartData(data);
        setProductList(data.cart_details.products);
      } catch (error) {
        console.error("Failed to fetch cart:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, []);

  const handleAddToCart = async (id: string, val: number) => {
    try {
      setLoading(true);
      const cartModify: ICartModify[] = [
        {
          product_id: id,
          quantity: val,
        },
      ];

      await cartAPIs.updateCart(cartModify);

      // Refresh cart data after update
      const updatedCart = await cartAPIs.getProductInCart();
      setCartData(updatedCart);
      setProductList(updatedCart.cart_details.products);
    } catch (error) {
      console.error("Failed to update cart:", error);
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
    total_price: `$${(product.total_price ?? 0).toFixed(2)}`,
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

  const handleCheckOut = async () => {
    try {
      if (!productlist || productlist.length === 0) {
        console.error("Cart is empty");
        return;
      }

      setLoading(true);
      const reqBody: IOrderProduct[] = productlist.map(
        ({ product_id, quantity }) => ({
          product_id,
          quantity,
        })
      );

      const res = await orderAPIs.checkout(reqBody);

      if (res.payment_url) {
        // Force redirect to payment URL
        window.location.replace(res.payment_url);
      } else {
        console.error("No payment URL received");
      }
    } catch (error) {
      console.error("Failed to process checkout:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col justify-center mx-64">
      <h1 className="flex gap-2 font-bold text-xl mb-4 mt-12">
        Cart
        <span className="text-[#939699] font-normal">
          ({!loading ? productlist?.length : 0})
        </span>
      </h1>

      {!loading ? (
        productlist?.length! > 0 ? (
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
          <div className="text-center py-52">Your cart is empty</div>
        )
      ) : (
        <ProductListInCartSkeleton />
      )}

      <Divider className="mb-8" />

      <div className="mb-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ChevronLeft size={18} className="text-[#BCBFC2]" />
          <p className="text-[#939699] font-bold">Back to shopping</p>
        </div>

        <div className="flex justify-between items-center mt-4 gap-4">
          <div className="text-xl font-bold">
            Total: ${cartData?.cart_details.total_price.toFixed(2) || "0.00"}
          </div>
          <Button
            className="bg-black text-white px-8 rounded-full"
            onClick={handleCheckOut}
          >
            Check out
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
