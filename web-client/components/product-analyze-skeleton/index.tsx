import {
  Skeleton,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from "@nextui-org/react";

const ProductAnalyzeSkeleton = () => {
  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <Skeleton className="h-8 w-32 rounded-lg" />
        <Skeleton className="h-10 w-32 rounded-lg" />
      </div>

      <Table aria-label="Loading table">
        <TableHeader>
          {[1, 2, 3, 4].map((_, index) => (
            <TableColumn key={index}>
              <Skeleton className="h-4 w-20 rounded-lg" />
            </TableColumn>
          ))}
        </TableHeader>
        <TableBody>
          {Array(5)
            .fill(null)
            .map((_, rowIndex) => (
              <TableRow key={rowIndex}>
                {Array(4)
                  .fill(null)
                  .map((_, colIndex) => (
                    <TableCell key={colIndex}>
                      <Skeleton className="h-20 w-full rounded-lg" />
                    </TableCell>
                  ))}
              </TableRow>
            ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default ProductAnalyzeSkeleton;
