"use client";

import React, { useState } from "react";
import { AgentsTable } from "./table/AgentsTable";
import { useAgents } from "@/api_hooks/useAgents";

function AgentsFeature() {
  const [page] = useState(0);

  const { data, isPending, error } = useAgents(page);

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (isPending) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <AgentsTable
        data={data}
        onRowClick={(row) => {
          console.log(row);
        }}
      />
    </div>
  );
}

export default AgentsFeature;
