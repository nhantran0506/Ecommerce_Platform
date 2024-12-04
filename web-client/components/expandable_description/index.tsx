import { useState, useMemo } from "react";
import { Button } from "@nextui-org/react";
import { ChevronDown, ChevronUp } from "react-feather";

interface ExpandableDescriptionProps {
  description: string;
  maxWords?: number;
}

const ExpandableDescription: React.FC<ExpandableDescriptionProps> = ({
  description,
  maxWords = 500,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const { shouldShowMore, displayText, fullText } = useMemo(() => {
    const words = description.split(/\s+/);
    const shouldShow = words.length > maxWords;
    const truncated = words.slice(0, maxWords).join(" ");
    
    return {
      shouldShowMore: shouldShow,
      displayText: shouldShow ? truncated + "..." : description,
      fullText: description
    };
  }, [description, maxWords]);

  return (
    <div className="w-full">
      <p className="text-gray-600 leading-relaxed">
        {isExpanded ? fullText : displayText}
      </p>
      
      {shouldShowMore && (
        <Button
          variant="light"
          className="mt-2"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <span className="flex items-center gap-2">
            {isExpanded ? (
              <>
                Show Less <ChevronUp size={20} />
              </>
            ) : (
              <>
                Show More <ChevronDown size={20} />
              </>
            )}
          </span>
        </Button>
      )}
    </div>
  );
};

export default ExpandableDescription; 