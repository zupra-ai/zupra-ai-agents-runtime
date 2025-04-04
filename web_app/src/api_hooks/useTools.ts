import ToolModel from "@/models/ToolModel";
import { useQuery } from "@tanstack/react-query";

/**
 * Custom hook for fetching a list of MyModel items from your API.
 *
 * @param page the current page number
 * @returns a React Query result object containing:
 *   - data: MyModel[] | undefined
 *   - isLoading: boolean
 *   - isError: boolean
 *   - error: Error | null
 */

export function useTools(page: number) {
  return useQuery<ToolModel[], Error>({
    queryKey: ["tools", page],
    queryFn: async () => {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_HOST}/tools?page=${page}`
      );
      if (!res.ok) {
        throw new Error("Network response was not OK");
      }
      return res.json().then((data) => {
        return data["data"] as ToolModel[];
      });
    },
  });
}
