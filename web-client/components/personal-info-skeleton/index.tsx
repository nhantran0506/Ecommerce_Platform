import { Card, Skeleton } from "@nextui-org/react";

const PersonalInfoSkeleton = () => {
  return (
    <Card className="p-6">
      <div className="flex items-center gap-6 mb-8">
        <Skeleton className="w-24 h-24 rounded-full" />
        <div>
          <Skeleton className="w-48 h-6 rounded-lg mb-2" />
          <Skeleton className="w-32 h-4 rounded-lg" />
        </div>
      </div>

      <div className="space-y-6">
        {Array(5)
          .fill(null)
          .map((_, index) => (
            <div key={index} className="flex flex-col gap-2">
              <Skeleton className="w-32 h-4 rounded-lg" />
              <Skeleton className="w-full h-12 rounded-lg" />
            </div>
          ))}
      </div>

      <div className="flex justify-end mt-8">
        <Skeleton className="w-32 h-10 rounded-lg" />
      </div>
    </Card>
  );
};

export default PersonalInfoSkeleton;
