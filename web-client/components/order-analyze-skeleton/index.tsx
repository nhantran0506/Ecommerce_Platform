import { Card, Skeleton } from "@nextui-org/react";

const OrderAnalyzeSkeleton = () => {
  return (
    <div className="grid grid-cols-2 gap-4">
      {Array(4)
        .fill(null)
        .map((_, index) => (
          <Card key={index} className="p-4">
            <div className="flex justify-between mb-4">
              <Skeleton className="w-24 h-6 rounded-lg" />
              <Skeleton className="w-32 h-6 rounded-lg" />
            </div>

            {Array(2)
              .fill(null)
              .map((_, itemIndex) => (
                <div key={itemIndex} className="flex items-center gap-4 mb-4">
                  <Skeleton className="w-20 h-20 rounded-lg" />
                  <div className="flex-1">
                    <Skeleton className="w-3/4 h-4 rounded-lg mb-2" />
                    <Skeleton className="w-1/4 h-4 rounded-lg" />
                  </div>
                </div>
              ))}

            <div className="flex justify-between mt-4">
              <Skeleton className="w-32 h-6 rounded-lg" />
              <Skeleton className="w-24 h-6 rounded-lg" />
            </div>
          </Card>
        ))}
    </div>
  );
};

export default OrderAnalyzeSkeleton;
