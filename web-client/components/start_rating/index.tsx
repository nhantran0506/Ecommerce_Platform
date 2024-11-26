// components/StarRating.tsx
import React, { useState } from "react";
import { Star } from "react-feather";

interface StarRatingProps {
  totalStars?: number;
  color?: string; // Add color prop to customize the star color
  initStart?: number;
}

const StarRating: React.FC<StarRatingProps> = ({
  totalStars = 5,
  color = "#eac086",
  initStart = 0,
}) => {
  // Default color to a custom value
  const [rating, setRating] = useState<number>(initStart ?? 0);
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
            // onClick={() => setRating(starValue)}
            // onMouseEnter={() => setHover(starValue)}
            // onMouseLeave={() => setHover(0)}
          >
            <Star
              size={15}
              fill={starValue <= (hover || rating) ? color : "gray"}
              color={starValue <= (hover || rating) ? color : "gray"}
            />
          </div>
        );
      })}
    </div>
  );
};

export default StarRating;
