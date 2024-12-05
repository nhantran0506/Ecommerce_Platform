import { Card, CardFooter, Skeleton } from "@nextui-org/react";

interface ListProductCardSkeletonProps {
  gridCols?: number;
  count?: number;
}

const ListProductCardSkeleton = ({
  gridCols,
  count = 3,
}: ListProductCardSkeletonProps) => {
  return (
    <div className={`grid grid-cols-${gridCols} gap-8`}>
      {Array.from({ length: count }).map((_, index) => (
        <Card className="border-2 rounded-xl w-[220px] h-[300px]" key={index}>
          <Skeleton className="overflow-visible p-0">
            <div className="w-full h-[180px] rounded-t-xl bg-default-300"></div>
          </Skeleton>
          <CardFooter>
            <div className="flex flex-col w-full h-full space-y-2">
              <Skeleton className="rounded-lg">
                <div className="h-6 w-3/4 rounded bg-default-200"></div>
              </Skeleton>
              <div className="flex justify-between items-center">
                <div className="flex flex-col items-start space-y-1">
                  <Skeleton className="rounded-lg">
                    <div className="h-5 w-1/3 rounded bg-default-200">
                      ............................
                    </div>
                  </Skeleton>
                  <Skeleton className="rounded-lg">
                    <div className="h-4 w-1/2 rounded bg-default-200">
                      ............................
                    </div>
                  </Skeleton>
                </div>
                <Skeleton className="w-10 h-10 rounded-full bg-default-200"></Skeleton>
              </div>
            </div>
          </CardFooter>
        </Card>
      ))}
    </div>
  );
};

export default ListProductCardSkeleton;
