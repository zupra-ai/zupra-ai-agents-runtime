"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";

function ApplicationsFeature() {
  const [page] = useState(0);

  const { isPending, error, data } = useQuery({
    queryKey: ["data", { page }],
    queryFn: () =>
      fetch(
        `${process.env.NEXT_PUBLIC_API_HOST}/applications?page=${page}`
      ).then((res) => res.json()),
  });

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (isPending) {
    return <div>Loading...</div>;
  }

  return <div>{JSON.stringify(data)}</div>;
}

export default ApplicationsFeature;
