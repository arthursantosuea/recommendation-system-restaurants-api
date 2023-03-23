import { SearchIcon } from "lucide-react";
import React, { useState } from "react";

interface SearchFieldProps {
  onGetRecommendations: (description: string) => void;
}

export function SearchField({ onGetRecommendations }: SearchFieldProps) {
  const [description, setDescription] = useState("");
  return (
    <div className="flex sm:w-[50%] w-[80%]">
      <input
        type="text"
        className="w-full mx-auto outline-none rounded-l-md text-sm h-8 pl-2 bg-[#f0f0f5]"
        placeholder="O que você deseja comer?"
        onChange={(event: React.FormEvent<HTMLInputElement>) =>
          setDescription(event.currentTarget.value)
        }
        onKeyDown={(event: React.KeyboardEvent<HTMLInputElement>) =>  event.key == "Enter" && onGetRecommendations(description)}
      />
      <SearchIcon
        strokeWidth={1}
        className="bg-[#f0f0f5] rounded-r-md h-8 w-8 p-1 hover:bg-slate-200 hover:transition-colors transition-colors hover:cursor-pointer"
        onClick={() => onGetRecommendations(description)}
      />
    </div>
  );
}
