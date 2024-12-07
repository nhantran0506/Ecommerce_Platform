import { Card, Skeleton } from "@nextui-org/react";

const PersonalInfoSkeleton = () => {
  return (
    <Card className="p-6">
      <div className="flex items-center gap-6 mb-8">
        <div>
          <Skeleton className="w-96 h-8 rounded-lg mb-2" />
        </div>
      </div>

      <div className="space-y-6">
        {Array(3)
          .fill(null)
          .map((_, index) => (
            <div key={index} className="flex flex-col gap-2">
              <Skeleton className="w-32 h-4 rounded-lg" />
              <Skeleton className="w-full h-12 rounded-lg" />
            </div>
          ))}
      </div>

      <div className="flex justify-start mt-8 gap-4">
        <Skeleton className="w-32 h-10 rounded-lg" />
        <Skeleton className="w-32 h-10 rounded-lg" />
      </div>
    </Card>
  );
};

export default PersonalInfoSkeleton;
