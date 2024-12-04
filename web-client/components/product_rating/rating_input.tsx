import { useState } from "react";
import { Button, Textarea, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, useDisclosure } from "@nextui-org/react";
import { Star } from "react-feather";

interface RatingInputProps {
  onSubmit: (rating: number, comment: string) => Promise<{ success: boolean; error?: string }>;
}

const RatingInput: React.FC<RatingInputProps> = ({ onSubmit }) => {
  const [rating, setRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [comment, setComment] = useState("");
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async () => {
    const result = await onSubmit(rating, comment);
    if (!result.success && result.error) {
      setErrorMessage(result.error);
      onOpen();
    } else {
      setRating(0);
      setComment("");
    }
  };

  return (
    <>
      <div className="w-full border rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-4">Write a Review</h3>
        
        <div className="flex gap-2 mb-4">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              onMouseEnter={() => setHoveredRating(star)}
              onMouseLeave={() => setHoveredRating(0)}
              onClick={() => setRating(star)}
            >
              <Star
                size={24}
                fill={(hoveredRating || rating) >= star ? "gold" : "none"}
                color={(hoveredRating || rating) >= star ? "gold" : "gray"}
              />
            </button>
          ))}
        </div>

        <Textarea
          placeholder="Share your thoughts about this product..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          className="mb-4"
        />

        <Button
          className="bg-black text-white"
          isDisabled={rating === 0}
          onClick={handleSubmit}
        >
          Submit Review
        </Button>
      </div>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalContent>
          <ModalHeader className="flex mb-1 gap-2 items-center text-2xl">
            Cannot Submit Review
          </ModalHeader>
          <ModalBody className="mb-2">
            <div>{errorMessage || "You need to purchase this product before leaving a review."}</div>
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onPress={onClose}>
              Ok
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default RatingInput; 