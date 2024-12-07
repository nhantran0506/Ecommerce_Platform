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
import { useTheme } from "next-themes";

export default function OrderDetailPageSkeleton() {
  const { theme } = useTheme();

  return (
    <div className="flex flex-col mx-60 my-10" data-theme={theme}>
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
          <Table removeWrapper aria-label="Skeleton table">
            <TableHeader>
              <TableRow>
                {[...Array(3)].map((_, index) => (
                  <TableColumn key={index}>
                    <Skeleton className="h-6 w-24 rounded-lg" />
                  </TableColumn>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {[...Array(3)].map((_, rowIndex) => (
                <TableRow key={rowIndex}>
                  {[...Array(3)].map((_, colIndex) => (
                    <TableCell key={colIndex}>
                      <Skeleton className="h-6 w-20 rounded-lg" />
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      </div>
    </div>
  );
}
