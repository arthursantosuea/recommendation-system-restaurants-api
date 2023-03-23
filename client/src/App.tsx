import { useState } from "react";

import { api } from "./services/api";
import {
  ArrowUpRightIcon,
  Loader2Icon,
  MapPinIcon,
  StarIcon,
} from "lucide-react";

import { SearchField } from "./components/SearchField";

interface IRecommendations {
  Name: string;
  City: string;
  Country: string;
  CuisineStyle: string;
  Rating: number;
  PriceRange: string;
  NumberOfReviews: number;
  Reviews: string[][];
  URL_TA: string;
}

export function App() {
  const [recommendations, setRecommendations] = useState<IRecommendations[]>(
    []
  );

  const [isLoading, setIsLoading] = useState(false);

  async function onGetRecommendations(desc: string) {
    setIsLoading(true);
    await api
      .post("/recommendation", { desc })
      .then((response) => {
        setIsLoading(false);
        setRecommendations(response.data);
        console.log(recommendations);
      })
      .catch((error) => {
        setIsLoading(false);
        console.log(error);
      });
  }

  function onRedirectForTripAdvisor(URL_TA: string) {
    window.open(`https://tripadvisor.com${URL_TA}`, "_blank", "noreferrer");
  }

  return (
    <div className="bg-[#03001C] max-w-screen min-h-screen flex flex-col items-center justify-center">
      <h1
        className={`text-white font-bold text-2xl ${
          recommendations && "mt-8"
        }`}
      >
        MoFomme
      </h1>
      <h3 className="text-white text-sm mb-10">
        Encontre a experiência gastronômica perfeita!
      </h3>
      <SearchField onGetRecommendations={onGetRecommendations} />
      <main className="flex items-center justify-center flex-wrap flex-col sm:flex-row max-w-[90%] my-8 gap-4">
        {recommendations && !isLoading ? (
          recommendations.map((recommendation, index) => (
            <div
              className="sm:w-[calc(20%-1rem)] w-[80%] h-60 bg-[#f0f0f5] flex flex-col justify-between shadow-sm rounded-md p-4"
              key={index}
            >
              <div className="flex flex-col">
                <div className="font-bold text-lg">{recommendation.Name}</div>
                <div className="flex items-center">
                  <MapPinIcon size={18} strokeWidth={1} className="mr-1" />
                  {recommendation.City}, {recommendation.Country}
                </div>
                <div className="flex items-center">
                  <StarIcon
                    size={20}
                    fill="#ffae00"
                    strokeWidth={0}
                    className="mr-1"
                  />
                  {recommendation.Rating} &#x2022; {recommendation.PriceRange}
                </div>
              </div>
              <div className="flex flex-wrap gap-1">
                {recommendation.CuisineStyle.split(",").map(
                  (cuisine, index) => (
                    <div
                      className="p-1 bg-slate-300 text-xs rounded-lg flex items-center"
                      key={index}
                    >
                      {cuisine}
                    </div>
                  )
                )}
              </div>
              <button
                className="bg-transparent text-[#03001C] flex items-center justify-between px-3 border-[1.5px] shadow-md font-normal h-8 w-[90%] border-black rounded-full hover:bg-[#03001C] hover:text-white hover:transition-colors transition-colors self-center"
                onClick={() => onRedirectForTripAdvisor(recommendation.URL_TA)}
              >
                Visitar
                <ArrowUpRightIcon size={20} />
              </button>
            </div>
          ))
        ) : (
          <Loader2Icon
            size={36}
            color="white"
            className="mt-4 animate-spin self-center"
          />
        )}
      </main>
    </div>
  );
}
