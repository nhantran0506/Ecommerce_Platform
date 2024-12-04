// components/StarRating.tsx
import React, { useState } from "react";
import { Star } from "react-feather";

interface StarRatingProps {
  totalStars?: number;
  color?: string;
  initStart?: number;
  readonly?: boolean;
}

const StarRating: React.FC<StarRatingProps> = ({
  totalStars = 5,
  color = "#eac086",
  initStart = 0,
  readonly = false,
}) => {
  const [rating, setRating] = useState<number>(initStart ?? 0);
  const [hover, setHover] = useState<number>(0);

  return (
    <div className="flex">
      {[...Array(totalStars)].map((_, index) => {
        const starValue = index + 1;
        return (
          <div
            key={index}
            role={readonly ? undefined : "button"}
            className="mr-1"
            onMouseEnter={() => !readonly && setHover(starValue)}
            onMouseLeave={() => !readonly && setHover(0)}
            onClick={() => !readonly && setRating(starValue)}
          >
            <Star
              size={15}
              fill={starValue <= (hover || rating) ? color : "none"}
              color={starValue <= (hover || rating) ? color : "gray"}
            />
          </div>
        );
      })}
    </div>
  );
};

export default StarRating;
