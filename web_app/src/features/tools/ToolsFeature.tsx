"use client";

import React, { useState } from "react";
import { AgentsTable } from "./table/AgentsTable";
import { useTools } from "@/api_hooks/useTools";
import ToolForm from "./form/ToolForm";
import ToolModel from "@/models/ToolModel";

function ToolsFeature() {
  const [page] = useState(0);
  const [tool, setTool] = useState<ToolModel | null>(null);

  const { data, isPending, error } = useTools(page);

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
          setTool(row);
        }}
      />

      {tool && (
        <ToolForm
          tool={tool}
          onOpenChange={() => {
            setTool(null);
          }}
        />
      )}
    </div>
  );
}

export default ToolsFeature;
