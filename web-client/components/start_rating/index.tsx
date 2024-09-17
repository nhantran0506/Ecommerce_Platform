// components/StarRating.tsx
import React, { useState } from "react";
import { Star } from "react-feather";

interface StarRatingProps {
  totalStars?: number;
}

const StarRating: React.FC<StarRatingProps> = ({ totalStars = 5 }) => {
  const [rating, setRating] = useState<number>(0);
  const [hover, setHover] = useState<number>(0);

  return (
    <div className="flex">
      {[...Array(totalStars)].map((_, index) => {
        const starValue = index + 1;
        return (
          <div
            key={index}
            role="button"
            className="mr-1"
            onClick={() => setRating(starValue)}
            onMouseEnter={() => setHover(starValue)}
            onMouseLeave={() => setHover(0)}
          >
            <Star
              size={24}
              fill={starValue <= (hover || rating) ? "yellow" : "none"}
              color={starValue <= (hover || rating) ? "yellow" : "gray"}
            />
          </div>
        );
      })}
    </div>
  );
};

export default StarRating;
