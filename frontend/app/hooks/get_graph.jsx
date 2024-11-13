import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import {API_ENDPOINT} from "../constants"

export const useGraphVariables = (independent, dependent) => {
  return useQuery({
    queryKey: ["graph", independent, dependent], // query key: graph is a label, independent and dependent are the variables
    queryFn: () => getGraphVariables(independent, dependent),
});
};

export const getGraphVariables = async (independent, dependent) => {
  const response = await axios.post(
    API_ENDPOINT,
    { independent, dependent },
  );
  return response.data;
};