import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import {API_ENDPOINT} from "../constants"

export const useSearch = (search, deleteFile) => {
  return useQuery({
    queryKey: ["search", search, deleteFile], // query key: graph is a label, independent and dependent are the variables
    queryFn: () => getSearch(search, deleteFile),
});
};

export const getSearch = async (search, deleteFile) => {
  const response = await axios.post(
    API_ENDPOINT,
    { search, deleteFile },
  );
  return response.data;
};