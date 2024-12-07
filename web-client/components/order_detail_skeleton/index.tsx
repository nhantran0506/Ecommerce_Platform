"use client";
import {
  Card,
  CardBody,
  CardFooter,
  Divider,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Skeleton,
} from "@nextui-org/react";

export default function OrderDetailPageSkeleton() {
  // Define columns structure
  const columns = [
    { key: "col1", label: "Column 1" },
    { key: "col2", label: "Column 2" },
    { key: "col3", label: "Column 3" },
  ];

  // Define rows structure
  const rows = [...Array(3)].map((_, index) => ({
    key: index,
    col1: <Skeleton className="h-6 w-20 rounded-lg" />,
    col2: <Skeleton className="h-6 w-20 rounded-lg" />,
    col3: <Skeleton className="h-6 w-20 rounded-lg" />,
  }));

  return (
    <div className="flex flex-col mx-60 my-10">
      <div className="mb-8">
        <Skeleton className="h-10 w-60 rounded-lg" />
      </div>

      <div className="mb-10">
        <Skeleton className="h-8 w-36 rounded-lg mb-4" />
        <Card>
          <CardBody>
            <div className="flex gap-4">
              {[...Array(3)].map((_, index) => (
                <Skeleton key={index} className="h-6 w-32 rounded-lg" />
              ))}
            </div>
          </CardBody>
          <Divider />
          <CardFooter className="flex justify-between">
            <Skeleton className="h-10 w-56 rounded-lg" />
            <Skeleton className="h-10 w-40 rounded-lg" />
          </CardFooter>
        </Card>
      </div>

      <div>
        <Skeleton className="h-8 w-36 rounded-lg mb-4" />
        <Card>
          <Table aria-label="Skeleton table" removeWrapper>
            <TableHeader columns={columns}>
              {(column) => (
                <TableColumn key={column.key}>
                  <Skeleton className="h-6 w-24 rounded-lg" />
                </TableColumn>
              )}
            </TableHeader>
            <TableBody items={rows}>
              {(item) => (
                <TableRow key={item.key}>
                  {(columnKey) => (
                    <TableCell>
                      {item[columnKey as keyof typeof item]}
                    </TableCell>
                  )}
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Card>
      </div>
    </div>
  );
}
