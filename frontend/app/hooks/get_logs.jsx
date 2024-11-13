import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import {API_ENDPOINT} from "../constants"

export const useLogs = (files, tosubmit) => {
    return useQuery({
        queryKey: ["logs", files, tosubmit], // query key: graph is a label, independent and dependent are the variables
        queryFn: () => getLogVariables(files, tosubmit),
    });
};

export const getLogVariables = async (files, tosubmit) => {
  const response = await axios.post(
    API_ENDPOINT,
    {files, tosubmit},
  );
  return response.data;
};