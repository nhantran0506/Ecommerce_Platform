import {
  Table,
  Skeleton,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from "@nextui-org/react";

const ProductListInCartSkeleton = () => {
  const columns = [
    { key: "item", label: "Item" },
    { key: "price", label: "Price" },
    { key: "quantity", label: "Quantity" },
    { key: "total_price", label: "Total Price" },
    { key: "options", label: "" },
  ];

  // Mocking the rows with placeholders for skeleton data
  const rows = new Array(5).fill(null).map((_, index) => ({
    key: `skeleton-${index}`,
    item: <Skeleton className="w-full h-6 rounded-lg bg-default-200" />,
    price: <Skeleton className="w-16 h-6 rounded-lg bg-default-200" />,
    quantity: (
      <div className="flex justify-center items-center">
        <Skeleton className="w-12 h-8 rounded-lg bg-default-200" />
      </div>
    ),
    total_price: <Skeleton className="w-16 h-6 rounded-lg bg-default-200" />,
  }));

  return (
    <div>
      <Table aria-label="Cart table" className="mb-8">
        <TableHeader columns={columns}>
          {(column) => (
            <TableColumn key={column.key}>
              <Skeleton className="text-sm w-40 h-6 rounded-lg bg-default-300" />
            </TableColumn>
          )}
        </TableHeader>
        <TableBody items={rows}>
          {(item) => (
            <TableRow key={item.key}>
              {(columnKey) => (
                <TableCell>
                  {columnKey === "options" ? (
                    <div className="flex justify-center w-full">
                      <Skeleton className="w-10 h-10 rounded-full bg-default-200" />
                    </div>
                  ) : (
                    <Skeleton className="w-32 h-8 rounded-lg bg-default-200" />
                  )}
                </TableCell>
              )}
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
};

export default ProductListInCartSkeleton;
