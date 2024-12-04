import { Star } from "react-feather";

interface RatingListProps {
  ratings: IProductRatingResponse[];
}

const RatingList: React.FC<RatingListProps> = ({ ratings }) => {
  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold mb-4">Customer Reviews</h3>
      
      <div className="space-y-4">
        {ratings.map((rating, index) => (
          <div key={index} className="border-b pb-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <p className="font-semibold">{rating.user_name}</p>
                <div className="flex gap-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                      key={star}
                      size={16}
                      fill={rating.rating >= star ? "gold" : "none"}
                      color={rating.rating >= star ? "gold" : "gray"}
                    />
                  ))}
                </div>
              </div>
              <span className="text-sm text-gray-500">
                {new Date(rating.created_at).toLocaleDateString()}
              </span>
            </div>
            
            {rating.comment && (
              <p className="text-gray-600 mt-2">{rating.comment}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default RatingList; 