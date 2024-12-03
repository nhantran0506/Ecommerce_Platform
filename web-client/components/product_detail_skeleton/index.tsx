import { Card, Skeleton } from "@nextui-org/react";

const ProductDetailSkeleton = () => {
  return (
    <div className="mx-64 grid grid-cols-2 mt-20">
      <div>
        <Skeleton className="rounded-lg w-[450px] h-[400px]" />
      </div>

      <div className="flex flex-col justify-between">
        <div className="px-2 pt-2">
          <div className="flex justify-between mb-4">
            <Skeleton className="w-2/3 h-8 rounded-lg" />
            <Skeleton className="w-9 h-9 rounded-full" />
          </div>

          <Skeleton className="w-1/3 h-8 mb-4 rounded-lg" />
          <Skeleton className="w-full h-20 mb-4 rounded-lg" />

          <div className="grid grid-cols-2 mb-4">
            {[1, 2, 3, 4].map((_, index) => (
              <div key={index} className="flex gap-2 mb-4">
                <Skeleton className="w-6 h-6 rounded-full" />
                <Skeleton className="w-24 h-6 rounded-lg" />
              </div>
            ))}
          </div>

          <div className="flex items-center gap-4">
            <Skeleton className="w-10 h-10 rounded-lg" />
            <Skeleton className="w-8 h-8 rounded-lg" />
            <Skeleton className="w-10 h-10 rounded-lg" />
          </div>
        </div>

        <div className="flex gap-4">
          <Skeleton className="w-1/2 h-12 rounded-full" />
          <Skeleton className="w-1/2 h-12 rounded-full" />
        </div>
      </div>
    </div>
  );
};

export default ProductDetailSkeleton;
