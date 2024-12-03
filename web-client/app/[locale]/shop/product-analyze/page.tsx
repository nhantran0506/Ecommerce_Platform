"use client";

import { useEffect, useState } from "react";
import productAPIs from "@/api/product";
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
  useDisclosure,
} from "@nextui-org/react";
import { PackagePlus, Trash2 } from "lucide-react";
import ProductMotificationPage from "./product-motification/page";
import { useProductId } from "@/state/state";
import SectionHeader from "@/components/section_header";
import ProductAnalyzeSkeleton from "@/components/product-analyze-skeleton";

const columns = [
  { key: "index", label: "Index" },
  { key: "item", label: "Item" },
  { key: "price", label: "Price" },
  { key: "action", label: "Actions" },
];

const ProductAnalyzePage = () => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const { setProductId } = useProductId();
  const [products, setProducts] = useState<IProductData[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const data = await productAPIs.getAllProductsShop();
        setProducts(data);
      } catch (error) {
        console.error("Failed to fetch shop products:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const rows = products.map((product, index) => ({
    key: product.product_id,
    index: index + 1,
    item: (
      <CartItemCard
        product={{
          ...product,
          quantity: 1,
          price: product.price,
        }}
        onClick={() => {
          setProductId(product.product_id);
          onOpen();
        }}
      />
    ),
    price: `$${product.price.toFixed(2)}`,
  }));

  if (loading) {
    return <ProductAnalyzeSkeleton />;
  }

  return (
    <>
      <SectionHeader
        title="Products"
        action={
          <Button
            className="text-white bg-black h-10"
            onPress={() => {
              setProductId("");
              onOpen();
            }}
          >
            <PackagePlus />
            <span>Create new</span>
          </Button>
        }
        content={
          <Table aria-label="Products table" className="mb-8">
            <TableHeader columns={columns}>
              {(column) => (
                <TableColumn key={column.key}>{column.label}</TableColumn>
              )}
            </TableHeader>
            <TableBody items={rows}>
              {(item) => (
                <TableRow key={item.key}>
                  {(columnKey) => (
                    <TableCell>
                      {columnKey === "action" ? (
                        <Button variant="light" color="danger" isIconOnly>
                          <Trash2 />
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
        }
      />

      <ProductMotificationPage isOpen={isOpen} onOpenChange={onOpenChange} />
    </>
  );
};

export default ProductAnalyzePage;
